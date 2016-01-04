# API Endpoints

[Template](https://gist.github.com/iros/3426278)


**Basic Functionality**

+ Create a user *(POST)*
+ Retrieve a node *(GET)*
+ Rank a node as a user *(POST)*
+ Map a connection between two nodes *(POST)*
+ Retrieve all nodes of a certain type *(GET)*  **NOT IMPLEMENTED**


**Retrieve a Node**
----
  Retrieve data for a specific node.

* **Method:**
  
  `GET`
  
* **URL**

  + `/api/user?id=string`
  + `/api/issue?id=string`
  + `/api/community?id=string`
  + `/api/value?id=string`
  + `/api/objective?id=string`
  + `/api/policy?id=string`
  
*  **URL Params**

   **Required:**
 
   `id=[string]`

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** `{ keys : values }`
 
* **Error Response:**

  * **Code:** 422 UNPROCESSABLE ENTITY <br />
    **Cause:** Invalid request parameters


**Rank an Entity**
----
  Assign rank as user to a given entity `Issue|Value|Objective|Policy`.

* **Method:**
  
  `POST`

* **URL**

  + `/api/rank/issue`
  + `/api/rank/value`
  + `/api/rank/objective`
  + `/api/rank/policy` 

* **Data Params**

  ```
  {
      user_id: [integer],
      node_id: [integer],   // must be valid `Value|Objective|Policy|Issue` node
      issue_id: [integer],  // not required if node to be ranked is of type `Issue` 
      rank: [integer]
  }
  ```
  
* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:**
      ```
      {
        success: [boolean],
        error: [string]     // present if success == False
      }
      ```
 
* **Error Response:**

  * **Code:** 422 UNPROCESSABLE ENTITY <br />
    **Cause:** Invalid request parameters


**Map two Entities**
----
  Create a user map between two entities `Value->Objective|Objective->Policy`.

* **Method:**
  
  `POST`

* **URL**

  + `/api/map/value/objective`
  + `/api/map/objective/policy`

* **Data Params**

  ```
  {
      user_id: [string],
      src_id: [string],
      dst_id: [string],
      strength: [integer]
  }
  ```
  
* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:**
      ```
      {
        success: [boolean],
        error: [string]     // present if success == False
      }
      ```
 
* **Error Response:**

  * **Code:** 422 UNPROCESSABLE ENTITY <br />
    **Cause:** Invalid request parameters


# TO IMPLEMENT

**Retrieve All Data for an Entity type**
----
  Retrieve all entities of a specific type for `Values|Objectives|Policies|Issues|Communities`.
  
* **Method:**
  
  `GET`  
  
* **URL**

  + `/api/values`
  + `/api/objectives?issue_id=integer`
  + `/api/policies?issue_id=integer`
  + `/api/issues?community_id=integer`
  + `/api/communities`

*  **URL Params**

   **Required:**
    + For `objectives` or `policies` requests `issue_id=[integer]` param is required
    + For `issues` requests `community_id=[integer]` param is required

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** `{ nodes : [ { id : [integer], ... }, ... ] }`
 
* **Error Response:**

  * **Code:** 422 UNPROCESSABLE ENTITY <br />
    **Cause:** Invalid request parameters
