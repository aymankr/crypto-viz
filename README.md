# Crypto-Viz

## Prerequisites

- docker (with compose)
- make

## 🧰 Setup

Once the project is cloned, copy the local .env file:
```bash
cp .env .env.local
```

Launch the dockerized services:
```bash
make
```

If services fail to start, restart them until the configuration is done.

> You can also specify a number of spark workers using the following command:
> ```bash
> make WORKERS=8
> ```

## 📊 Connecting Power BI to the PostgreSQL Database

Follow these steps to connect Power BI to the PostgreSQL database and visualize your data.

### Prerequisites

Ensure the PostgreSQL database is running.

Check the `.env` file in your project root directory and note the following parameters:

- **POSTGRES_PORT**: The port on which the PostgreSQL database is exposed.
- **DATABASE_NAME**: The name of your database.
- **DATABASE_USERNAME**: The username for your database.
- **DATABASE_PASSWORD**: The password for your database user.

Ensure the Npgsql PostgreSQL connector is installed in Power BI.

### Steps to Connect

1. **Launch Power BI Desktop:**
   - Open Power BI Desktop on your computer.
   
2. **Navigate to the PostgreSQL Connection Wizard:**
   - Click on **Get Data** in the toolbar.
   - Select **Database > PostgreSQL database** from the list and click **Connect**.

3. **Enter Connection Details:**
   - **Server**: `localhost`
   - **Port**: Enter the value of **POSTGRES_PORT** from your `.env` file (e.g., 5432).
   - **Database**: Enter the value of **DATABASE_NAME**.

4. **Enter Authentication Credentials:**
   - **Username**: Enter the value of **DATABASE_USERNAME**.
   - **Password**: Enter the value of **DATABASE_PASSWORD**.

5. **Load Data:**
   - Click **OK** to establish the connection.
   - Select the desired tables or queries from the database schema.
   - Click **Load** to import the data into Power BI.

## 📸 Visualizations

### Power BI Screenshots

Below are the screenshots of the Power BI visualizations showcasing different aspects of the analysis:

- **Screen 1: Market overview**
  
  ![1](https://github.com/user-attachments/assets/3490a0fc-536a-43c0-b2c1-c613f9cc7ca9)

- **Screen 2: Detailed overview for crypto**
  
  ![2](https://github.com/user-attachments/assets/f950a90a-c693-43d7-85e7-4080a9fefece)

- **Screen 3: Crypto variation analysis**
  
  ![3](https://github.com/user-attachments/assets/64587f4e-0f23-4514-9baf-7569f81312df)

- **Screen 4: Compare two cryptos**
  
  ![4](https://github.com/user-attachments/assets/71c9f7ac-b099-4989-a875-c16ec5204a7a)
  

### Grafana Dashboards

The following images show the results of our Grafana dashboards, where we tested different configurations by increasing the number of workers while decreasing the sleep time and buffer size to analyze system performance:

- **Grafana Dashboard - 3 Workers**
  ![grafana_workers_3](https://github.com/user-attachments/assets/7eb8445c-7d96-4695-a660-ab96707748dc)
- **Grafana Dashboard - 5 Workers**
  ![grafana_workers_5](https://github.com/user-attachments/assets/2307c8ef-ca72-4bab-8809-dcce41d57b0b)
- **Grafana Dashboard - 7 Workers**
  ![grafana_workers_7](https://github.com/user-attachments/assets/2796b7be-df44-4dab-b53f-f3a35e61bbac)
- **Grafana Dashboard - 9 Workers**
  ![grafana_workers_9](https://github.com/user-attachments/assets/8a4f96e4-8348-4c2e-8650-5c8c42002554)
- **Grafana Dashboard - 15 Workers**
  ![grafana_workers_15](https://github.com/user-attachments/assets/ba977f3d-c641-4809-be29-0bf5742a0142)
- **Grafana Dashboard - 30 Workers (Start Phase)**
  ![grafana_workers_30_start](https://github.com/user-attachments/assets/b12734f6-f5e6-49df-9e5c-fca2cd04f98d)
- **Grafana Dashboard - 30 Workers (Mid Phase)**
  ![grafana_workers_30_mid](https://github.com/user-attachments/assets/44310f64-5c70-4d4f-892d-7ea171d09245)
- **Grafana Dashboard - 30 Workers (End Phase)**
  ![grafana_workers_30_3](https://github.com/user-attachments/assets/5216f6cc-39c4-47ff-83aa-81fb8b3aeaa7)

### Hardware Configuration for Grafana Performance Testing

To conduct the performance tests in Grafana, we used the following system configuration:

- **Laptop:** HP ZBook 15 G6
- **Processor:** Intel i7 (9th Gen)
- **Memory:** 48 GB RAM

We increased the number of workers progressively while reducing the sleep time and buffer size to measure how the system handled different workloads. The Grafana dashboards provide insights into the system’s behavior under different loads.
