# JobTread API Documentation

## Overview
The JobTread API is based off the Pave query-language. Pave is a query language similar to GraphQL that allows you to query exactly what you need, and nothing more.

## Webhooks
Webhooks are a powerful tool to extend the functionality of our app, providing real-time updates about specific events occurring within the system. This works by sending a detailed POST request to the user-defined URL when these events are triggered.

Events could range from file uploads, task updates, customer creation, or any significant actions you'd like to monitor. To configure webhooks, navigate to the Webhooks page.

## Getting Started

### API Explorer
The API Explorer consists of three panes that provide a user-friendly interface to interact with our API without writing any code. The Schema Pane allows you to explore the JobTread API types and operations. Simply click on an object to learn about its fields and inputs.

You can write and execute queries directly in the Query Pane. We recommend running some of the example queries below to familiarize yourself with how our API works.

To begin, you will need to find your organization ID. Copy and paste the query below into the Query Pane and hit run to find it out.

#### My Organizations
```pave
currentGrant:
  user:
    id: {}
    name: {}
    memberships:
      nextPage: {}
      nodes:
        id: {}
        organization:
          id: {}
          name: {}
```

Once you have determined your organization ID, enter it below to auto-fill the example queries:
`22NjXYfAJr7p`

## Authentication

### Grants
The JobTread API uses grants to authenticate requests. Head to the grant management page to create new grants. Upon creation, the grant key will be displayed one time so that you can copy and use it to authenticate future requests.

### Using Grants
Once you have your grant key, you can interact with the API by making POST requests to https://api.jobtread.com/pave. To try this out, add your grant key to the request below and run in your local terminal.

#### cURL Request
```bash
curl https://api.jobtread.com/pave -d '{
  "query": {
    "$": { "grantKey": "{{YOUR_GRANT_KEY}}" },
    "currentGrant": { "id": {} }
  }
}'
```

## Querying

### Basic Query Structure
Inputs are passed as an object following the $ symbol. Fields to be returned are added at the same nested level as the input property. The _type field on each object in the response tells you its schema type.

Feel free to play around with the examples below to familiarize yourself with how our API works.

To create a customer or vendor we will look at the createAccount operation. The three required fields required to create an account are: organizationId, name and type.

#### Create Customer
```pave
createAccount:
  $:
    organizationId: 22NjXYfAJr7p
    name: Test Name
    type: customer
  createdAccount:
    id: {}
    name: {}
    createdAt: {}
    type: {}
    organization:
      id: {}
      name: {}
```

#### Create Vendor
```pave
createAccount:
  $:
    organizationId: 22NjXYfAJr7p
    name: Test Name
    type: vendor
  createdAccount:
    id: {}
    name: {}
    createdAt: {}
    type: {}
    organization:
      id: {}
      name: {}
```

After creating your accounts, you will see its id in the response at: createAccount.createdAccount.id. Using this id we can now read, update and delete this account.

#### Query Customer
```pave
account:
  $:
    id: "{{CREATED_ACCOUNT_ID}}"
  id: {}
  name: {}
  isTaxable: {}
  type: {}
```

#### Update Customer
```pave
updateAccount:
  $:
    id: "{{CREATED_ACCOUNT_ID}}"
    isTaxable: false
  account:
    $:
      id: "{{CREATED_ACCOUNT_ID}}"
    id: {}
    name: {}
    isTaxable: {}
```

#### Delete Customer
```pave
deleteAccount:
  $:
    id: "{{CREATED_ACCOUNT_ID}}"
```

#### Connection Fields
Objects that share one or more properties can be queried simultaneously as connection fields. For example, all accounts share the organizationId field. Because of this, we can query all accounts that belong to a specific organization by querying the nodes on its accounts field.

#### Find Accounts
```pave
organization:
  $:
    id: 22NjXYfAJr7p
  id: {}
  accounts:
    nextPage: {}
    nodes:
      id: {}
      name: {}
      type: {}
```

We can use Pave to paginate the returned data by adding input arguments such as size to specify the return size, and page to specify the current page. Make sure to query nextPage and previousPage.

#### Find Accounts Paginated
```pave
organization:
  $:
    id: 22NjXYfAJr7p
  id: {}
  accounts:
    $:
      size: 5
      page: "{{PAGE_ID}}"
    nextPage: {}
    previousPage: {}
    nodes:
      id: {}
      name: {}
      type: {}
```

Pass the sortBy input to specify the order of your nodes. In this instance, we are asking for all accounts (page limit 5) starting with the vendors alphabetically and then the customers alphabetically.

#### Find Accounts Sorted
```pave
organization:
  $:
    id: 22NjXYfAJr7p
  id: {}
  accounts:
    $:
      size: 5
      sortBy:
        - field: type
          order: desc
        - field: name
    nextPage: {}
    previousPage: {}
    nodes:
      id: {}
      name: {}
      type: {}
```

#### Additional Query Modification
We can also use Pave to search for objects by the values of their fields by adding the where input. Let's find all accounts with the name "Test Name".

#### Find Account
```pave
organization:
  $:
    id: 22NjXYfAJr7p
  id: {}
  accounts:
    $:
      where:
        - name
        - =
        - Test Name
    nodes:
      id: {}
      name: {}
      type: {}
```

The where input field is very powerful and can handle multiple conditions. For instance, we modify the query above to return only accounts of the Customer type by adding an and operator.

#### Find Customer
```pave
organization:
  $:
    id: 22NjXYfAJr7p
  id: {}
  accounts:
    $:
      where:
        and:
          - - name
            - =
            - Test Name
          - - type
            - =
            - customer
    nodes:
      id: {}
      name: {}
      type: {}
```

In addition, we can use the or operator. To demonstrate, we will query all accounts of the customer or vendor type.

#### Find Customer/Vendor
```pave
organization:
  $:
    id: 22NjXYfAJr7p
  id: {}
  accounts:
    $:
      where:
        or:
          - - type
            - =
            - customer
          - - type
            - =
            - vendor
    nodes:
      id: {}
      name: {}
      type: {}
```

As with sorting, these operators can be chained together to form logic. Below we query all accounts that are of type: customer and that have the name "Test Name" or "Test Name2".

#### Find Account Modified
```pave
organization:
  $:
    id: 22NjXYfAJr7p
  id: {}
  accounts:
    $:
      where:
        and:
          - - type
            - =
            - customer
          - or:
              - - name
                - =
                - Test Name
              - - name
                - =
                - Test Name2
    nodes:
      id: {}
      name: {}
      type: {}
```

The where input can search deeper than the top-level targets by nesting a target path array inside the condition. For example, create a location for our customer. Then we will query all locations whose account.name is "Test Name".

#### Create Location
```pave
createLocation:
  $:
    accountId: "{{CREATED_ACCOUNT_ID}}"
    name: Test Location
    address: 12750 Merit Dr, Dallas, TX 75251
  createdLocation:
    id: {}
    name: {}
    address: {}
    account:
      id: {}
      name: {}
    createdAt: {}
```

#### Find Locations
```pave
organization:
  $:
    id: 22NjXYfAJr7p
  id: {}
  locations:
    $:
      where:
        - - account
          - name
        - Test Name
    nodes:
      id: {}
      name: {}
      address: {}
      account:
        id: {}
        name: {}
```

Putting it all together.

#### Find Locations Modified
```pave
organization:
  $:
    id: 22NjXYfAJr7p
  id: {}
  locations:
    $:
      where:
        or:
          - - - account
              - name
            - Test Name
          - - createdAt
            - ">"
            - 2023-01-01
      sortBy:
        - field: name
      size: 5
    nodes:
      id: {}
      name: {}
      address: {}
      account:
        id: {}
        name: {}
    nextPage: {}
```

#### Common Queries

#### Get custom fields for organization
```pave
organization:
  $:
    id: 22NjXYfAJr7p
  id: {}
  customFields:
    $:
      sortBy:
        - field: targetType
        - field: position
    nodes:
      id: {}
      name: {}
      type: {}
      targetType: {}
```

Add this query as a field on supported schema.

#### Get Custom Field Values
```pave
customFieldValues:
  $:
    size: 25
  nodes:
    id: {}
    value: {}
    customField:
      id: {}
```

For example, to get custom fields on a customer:

#### Get Account Custom Field Values
```pave
account:
  $:
    id: "{{CREATED_ACCOUNT_ID}}"
  id: {}
  name: {}
  isTaxable: {}
  type: {}
  customFieldValues:
    $:
      size: 25
    nodes:
      id: {}
      value: {}
      customField:
        id: {}
```

To update custom field values, pass the id of the custom field as the key and the value as the value. For example, to update custom fields on an account:

#### Update Account Custom Fields
```pave
updateAccount:
  $:
    id: "{{CREATED_ACCOUNT_ID}}"
    customFieldValues:
      "{{CUSTOM_FIELD_ID}}": "{{CUSTOM_FIELD_VALUE}}"
  account:
    $:
      id: "{{CREATED_ACCOUNT_ID}}"
    id: {}
    name: {}
    customFieldValues:
      $:
        size: 25
      nodes:
        id: {}
        value: {}
        customField:
          id: {}
```

Search by custom field values.

#### Search By Custom Field Values
```pave
organization:
  $:
    id: 22NjXYfAJr7p
  id: {}
  contacts:
    $:
      with:
        cf:
          _: customFieldValues
          $:
            where:
              - - customField
                - name
              - "{{CUSTOM_FIELD_NAME}}"
          values:
            $:
              field: value
      where:
        - - cf
          - values
        - =
        - "{{CUSTOM_FIELD_VALUE}}"
    nodes:
      id: {}
      name: {}
```

Search by multiple custom field values. Note, the keys in the where and if blocks must match.

#### Search By Multiple Custom Field Values
```pave
organization:
  $:
    id: 22NjXYfAJr7p
  id: {}
  contacts:
    $:
      with:
        cf1:
          _: customFieldValues
          $:
            where:
              - - customField
                - name
              - "{{CUSTOM_FIELD_NAME}}"
          values:
            $:
              field: value
        cf2:
          _: customFieldValues
          $:
            where:
              - - customField
                - name
              - "{{CUSTOM_FIELD_2_NAME}}"
          values:
            $:
              field: value
      where:
        or:
          - - - cf1
              - values
            - "{{CUSTOM_FIELD_VALUE}}"
          - - - cf2
              - values
            - "{{CUSTOM_FIELD_2_VALUE}}"
    nodes:
      id: {}
      name: {}
```

#### Get job summary fields.
```pave
job:
  $:
    id: "{{JOB_ID}}"
  id: {}
  documents:
    $:
      where:
        or:
          - and:
              - - type
                - bidRequest
              - - status
                - pending
          - and:
              - - type
                - vendorOrder
              - - status
                - in
                - - pending
                  - approved
          - and:
              - - type
                - customerOrder
              - - status
                - in
                - - pending
                  - approved
              - - includeInBudget
                - true
          - and:
              - - type
                - vendorBill
              - - status
                - in
                - - draft
                  - pending
          - and:
              - - type
                - customerInvoice
              - - status
                - in
                - - pending
                  - approved
      group:
        by:
          - type
          - status
        aggs:
          amountPaid:
            sum: amountPaid
          cost:
            sum: cost
          count:
            count: []
          priceWithTax:
            sum: priceWithTax
    withValues: {}
```

#### Get document pdf url. Append this pdf token to https://api.jobtread.com/t/ for the full URL.
```pave
pdfToken:
  _: signQuery
  $:
    query:
      pdf:
        $:
          id: document
          options:
            id: "{{DOCUMENT_ID}}"
```

#### Get documents by specific name.
```pave
organization:
  $:
    id: 22NjXYfAJr7p
  id: {}
  documents:
    $:
      where:
        or:
          - - name
            - Expense
          - - name
            - Bill
    nodes:
      id: {}
      name: {}
      type: {}
```

#### Get open invoices.
```pave
organization:
  $:
    id: 22NjXYfAJr7p
  id: {}
  documents:
    $:
      where:
        and:
          - - type
            - customerInvoice
          - - status
            - pending
          - - price
            - ">"
            - 0
      sortBy:
        - field: price
          order: desc
      size: 5
    nodes:
      id: {}
      cost: {}
      price: {}
      tax: {}
      name: {}
      number: {}
      job:
        id: {}
        name: {}
        number: {}
    nextPage: {}
```

#### Sum approved customer orders on a job.
```pave
job:
  $:
    id: "{{JOB_ID}}"
  documents:
    $:
      where:
        and:
          - - type
            - customerOrder
          - - status
            - approved
          - - includeInBudget
            - true
    sum:
      $: priceWithTax
```

#### FAQ
Why am I getting "id field required"?
You must query the id field for each object you would like to be returned.