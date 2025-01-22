### **README: Heymarket Crawler API**

This API provides endpoints to process, fetch, and retrieve data related to Heymarket lists and reports. Below are the details of the available endpoints, their usage, sample requests, and responses.

---

## **Base URL**
```
http://heymarket-crawler.nq54xjgsjmjxc.eu-west-1.cs.amazonlightsail.com/
```

---

### **Endpoints**

#### **1. Process a List**
**Endpoint:** `/process_list`  
**Method:** `POST`

**Description:**  
Processes a Heymarket list asynchronously by scraping the data.

**Request Body:**
```json
{
   "list_id": 1174814,
   "message_content": "hey this message will sent at 9:25 edit check",
   "username": "your_username",
   "password": "_your_password_",
   "message_timestamp":"January 22nd, 2025 at 9:25 PM"
 }
```

**Response:**
```json
{
  "message": "Request submitted successfully. Scraping is in progress."
}
```

---

#### **2. Get All Data**
**Endpoint:** `/get_all_data`  
**Method:** `GET`

**Description:**  
Fetches all scraped data from the database.

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "List_id": 1174814,
      "List_name": "Test List haymarket Dummy",
      "Msg_heading": "Message sent on January 22nd, 2025 at 4:35 AM",
      "Content": "This message will sent at 4 : 35",
      "Campaign": "Campaign 2 Test",
      "send_to": "Sent to 1 Contacts",
      "deliverd": ["(616) 314-2136"],
      "failed": [],
      "responded": [],
      "opt_out": [],
      "reports": {
        "Delivered Messages": "1",
        "Failed Messages": "0",
        "Response Rate": "0%",
        "Opt Out Rate": "0%"
      },
      "report_id": 1702123,
      "created_at": "2025-01-22T04:35:00"
    }
  ],
  "message": "Data fetched successfully."
}
```

---

#### **3. Get Last Data**
**Endpoint:** `/get_last_data`  
**Method:** `GET`

**Description:**  
Fetches the most recent record from the database.

**Response:**
```json
{
  "data": {
    "id": 1,
    "List_id": 1174814,
    "List_name": "Test List haymarket Dummy",
    "Msg_heading": "Message sent on January 22nd, 2025 at 4:35 AM",
    "Content": "This message will sent at 4 : 35",
    "Campaign": "Campaign 2 Test",
    "send_to": "Sent to 1 Contacts",
    "deliverd": ["(616) 314-2136"],
    "failed": [],
    "responded": [],
    "opt_out": [],
    "reports": {
      "Delivered Messages": "1",
      "Failed Messages": "0",
      "Response Rate": "0%",
      "Opt Out Rate": "0%"
    },
    "report_id": 1702123,
    "created_at": "2025-01-22T04:35:00"
  },
  "message": "Latest data fetched successfully."
}
```

---

#### **4. Get Campaign Data**
**Endpoint:** `/get_campaign_data`  
**Method:** `POST`

**Description:**  
Fetches all data for a specific campaign name.

**Request Body:**
```json
{
  "campaign": "Campaign 2 Test"
}
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "List_id": 1174814,
      "List_name": "Test List haymarket Dummy",
      "Msg_heading": "Message sent on January 22nd, 2025 at 4:35 AM",
      "Content": "This message will sent at 4 : 35",
      "Campaign": "Campaign 2 Test",
      "send_to": "Sent to 1 Contacts",
      "deliverd": ["(616) 314-2136"],
      "failed": [],
      "responded": [],
      "opt_out": [],
      "reports": {
        "Delivered Messages": "1",
        "Failed Messages": "0",
        "Response Rate": "0%",
        "Opt Out Rate": "0%"
      },
      "report_id": 1702123,
      "created_at": "2025-01-22T04:35:00"
    }
  ],
  "message": "Data fetched successfully for campaign 'Campaign 2 Test'."
}
```

---

#### **5. Get Data by Report ID**
**Endpoint:** `/get_report_data`  
**Method:** `POST`

**Description:**  
Fetches all data for a specific `report_id`.

**Request Body:**
```json
{
  "report_id": 1702123
}
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "List_id": 1174814,
      "List_name": "Test List haymarket Dummy",
      "Msg_heading": "Message sent on January 22nd, 2025 at 4:35 AM",
      "Content": "This message will sent at 4 : 35",
      "Campaign": "Campaign 2 Test",
      "send_to": "Sent to 1 Contacts",
      "deliverd": ["(616) 314-2136"],
      "failed": [],
      "responded": [],
      "opt_out": [],
      "reports": {
        "Delivered Messages": "1",
        "Failed Messages": "0",
        "Response Rate": "0%",
        "Opt Out Rate": "0%"
      },
      "report_id": 1702123,
      "created_at": "2025-01-22T04:35:00"
    }
  ],
  "message": "Data fetched successfully for report_id '1702123'."
}
```

---

#### **6. Get Data by List ID**
**Endpoint:** `/get_list_data`  
**Method:** `POST`

**Description:**  
Fetches all data for a specific `list_id`.

**Request Body:**
```json
{
  "list_id": 1174814
}
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "List_id": 1174814,
      "List_name": "Test List haymarket Dummy",
      "Msg_heading": "Message sent on January 22nd, 2025 at 4:35 AM",
      "Content": "This message will sent at 4 : 35",
      "Campaign": "Campaign 2 Test",
      "send_to": "Sent to 1 Contacts",
      "deliverd": ["(616) 314-2136"],
      "failed": [],
      "responded": [],
      "opt_out": [],
      "reports": {
        "Delivered Messages": "1",
        "Failed Messages": "0",
        "Response Rate": "0%",
        "Opt Out Rate": "0%"
      },
      "report_id": 1702123,
      "created_at": "2025-01-22T04:35:00"
    }
  ],
  "message": "Data fetched successfully for list_id '1174814'."
}
```

---

### **Notes**
- Ensure all required fields are included in the request.
- Proper authentication and validation are recommended for production environments.

