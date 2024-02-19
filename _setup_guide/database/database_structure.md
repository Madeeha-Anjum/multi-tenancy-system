# Database Setup information

   **Table Creation:** Necessary tables for the application are created in the database.

   **Postgres Schema Separation**:
   Each tenant or company can have its own schema if there is a tenant create in teh shared.tenants table.
   Example: <http://company1.yourapp.com> and <http://company2.yourapp.com>  

**Default Schemas:**
    There are two default schemas created in the database:
    - Shared Schema: Used for tenant-specific data (default: `shared`).
    - Tenant Default Schema: Default schema if one is not provided (default: `tenant_default`). For example if there is no schema for a tenant, the application will use this schema

    +-------------------+
    |                   |
    |    shared         |
    |    schema         |
    |                   |
    |   +-------------+ |
    |   |  tenants    | |
    |   |   table     | |
    |   +-------------+ |
    +-------------------+

    +-------------------+
    |                   |
    | tenant_default    |
    |    schema         |
    |                   |
    +-------------------+
