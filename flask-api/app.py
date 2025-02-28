from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import os, enum, logging
from datetime import datetime

db = SQLAlchemy()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]

CORS(app)
db.init_app(app)

# Set up logging
logging.basicConfig(level=logging.INFO)


# -------------
# Define Models
# -------------

class CryptoItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    symbol = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    scraped_at = db.Column(db.DateTime, nullable=False)

    volume_24h = db.Column(db.Float, nullable=True)
    change_1h = db.Column(db.Float, nullable=True)
    change_24h = db.Column(db.Float, nullable=True)
    change_7d = db.Column(db.Float, nullable=True)
    market_cap = db.Column(db.Float, nullable=True)
    circulating_supply = db.Column(db.Float, nullable=True)
    rank = db.Column(db.Integer, nullable=True)
    logo_url = db.Column(db.String, nullable=True)

    __tablename__ = "crypto_items"
    __table_args__ = (
        db.UniqueConstraint(
            "name", "symbol", "scraped_at", name="uniq_name_symbol_scraped_at"
        ),
    )

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "symbol": self.symbol,
            "price": self.price,
            "scraped_at": self.scraped_at.isoformat(),
            "volume_24h": self.volume_24h,
            "change_1h": self.change_1h,
            "change_24h": self.change_24h,
            "change_7d": self.change_7d,
            "market_cap": self.market_cap,
            "circulating_supply": self.circulating_supply,
            "rank": self.rank,
            "logo_url": self.logo_url
        }


class LogIssuer(enum.Enum):
    SCRAPY = "SCRAPY"
    KAFKA = "KAFKA"
    SPARK_MASTER = "SPARK_MASTER"
    SPARK_WORKER = "SPARK_WORKER"
    FLASK_API = "FLASK_API"


class LogLevel(enum.Enum):
    INFO = "INFO"
    ERROR = "ERROR"


class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issuer = db.Column(db.Enum(LogIssuer), nullable=False)
    message = db.Column(db.String, nullable=False)
    level = db.Column(db.Enum(LogLevel), nullable=False)

    # Timestamp
    issued_at = db.Column(db.DateTime, nullable=False)

    # Spark worker id (docker hostname)
    worker_id = db.Column(db.String, nullable=True)

    # Spark session start time, used to identify the logs for a specific session
    session_start = db.Column(db.DateTime, nullable=True)

    __tablename__ = "logs"

    def jsonify(self):
        """
        Return a JSON representation of the object
        """
        return {
            "id": self.id,
            "issuer": self.issuer.value,
            "message": self.message,
            "level": self.level.value,
            "issued_at": self.issued_at.isoformat(),
            "worker_id": self.worker_id,
            "session_start": self.session_start,
        }


# -------------
# Create Tables
# -------------
with app.app_context():
    db.create_all()


# -------------
# Define Routes
# -------------
@app.route("/api/crypto-items", methods=["POST"])
def create_crypto_item():
    data = request.json

    if data is None:
        return jsonify({"error": "No data provided"}), 400

    logging.info(f"data={data}")

    try:
        # On utilise scraped_at fourni par le spider
        item = CryptoItems(
            name=data["name"],
            symbol=data["symbol"],
            price=data["price"],
            scraped_at=datetime.fromisoformat(data["scraped_at"]),
            volume_24h=data.get("volume_24h"),
            change_1h=data.get("change_1h"),
            change_24h=data.get("change_24h"),
            change_7d=data.get("change_7d"),
            market_cap=data.get("market_cap"),
            circulating_supply=data.get("circulating_supply"),
            rank=data.get("rank"),
            logo_url=data.get("logo_url")
        )

        db.session.add(item)
        db.session.commit()

        logging.info(f"Data inserted successfully: {data}")
        return jsonify({"data": item.jsonify()}), 201

    except Exception as e:
        logs = Logs(
            issuer=LogIssuer.FLASK_API,
            message=str(e),
            level=LogLevel.ERROR,
            issued_at=datetime.now(),
        )

        db.session.add(logs)
        db.session.commit()

        logging.error(f"Error inserting data: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500



@app.route("/api/logs", methods=["POST"])
def create_logs():
    data = request.json

    if data is None:
        # Return an error if no data is provided
        return jsonify({"error": "No data provided"}), 400

    try:
        log = Logs(
            issuer=data["issuer"],
            message=data["message"],
            level=data["level"],
            issued_at=datetime.fromisoformat(data["issued_at"]),
            # Optional fields
            session_start=data.get("session_start", None),
            worker_id=data.get("worker_id", None),
        )

        db.session.add(log)
        db.session.commit()

        return jsonify({"data": log.jsonify()}), 201

    except Exception as e:
        logging.error(f"Error inserting data: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)