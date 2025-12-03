---
layout: default
title: Wrapper Class Patterns
description: Patterns for using Apex wrapper classes to shape data for UI, batch processing, and integrations
permalink: /rag/development/wrapper-classes-patterns.html
---

## What Was Actually Done

- Used wrapper classes to combine data from multiple objects for LWCs, Aura, and Visualforce pages.
- Wrapped SObject records with extra flags (e.g., `isSelected`, `hasError`) for user selection and validation flows.
- Created lightweight DTO-style wrappers for integrations to control exactly what fields are serialized to JSON.
- Used wrappers in Batch Apex to carry additional state between `start`, `execute`, and `finish` when needed.

## Patterns

### Pattern 1: UI Selection Wrapper

**When to use**: You need additional UI-only state such as selection or error flags.

```apex
public class ContactSelectionWrapper {
    @AuraEnabled public Contact record { get; set; }
    @AuraEnabled public Boolean isSelected { get; set; }
    @AuraEnabled public Boolean hasError { get; set; }
    @AuraEnabled public String errorMessage { get; set; }

    public ContactSelectionWrapper(Contact record) {
        this.record = record;
        this.isSelected = false;
        this.hasError = false;
    }
}
```

### Pattern 2: Aggregated Data Wrapper

**When to use**: You must present combined data from multiple objects or queries.

```apex
public class AccountSummaryWrapper {
    @AuraEnabled public Id accountId { get; set; }
    @AuraEnabled public String accountName { get; set; }
    @AuraEnabled public Integer contactCount { get; set; }
    @AuraEnabled public Decimal totalOpenAmount { get; set; }
}
```

Service constructing the wrapper:
```apex
public with sharing class AccountSummaryService {
    @AuraEnabled(cacheable=true)
    public static List<AccountSummaryWrapper> getAccountSummaries() {
        List<AccountSummaryWrapper> summaries = new List<AccountSummaryWrapper>();

        // Example pattern: one SOQL with aggregates per account
        for (AggregateResult ar : [
            SELECT AccountId accId,
                   COUNT(Id) contactCount
            FROM Contact
            WHERE AccountId != null
            GROUP BY AccountId
        ]) {
            AccountSummaryWrapper w = new AccountSummaryWrapper();
            w.accountId = (Id) ar.get('accId');
            w.contactCount = (Integer) ar.get('contactCount');
            // Additional queries or cached data to populate name and totals
            summaries.add(w);
        }
        return summaries;
    }
}
```

### Pattern 3: Integration DTO Wrapper

**When to use**: You need strict control over serialized payloads for REST/SOAP integrations.

```apex
public class ContactSyncDTO {
    public String externalId;
    public String firstName;
    public String lastName;
    public String email;

    public static ContactSyncDTO fromContact(Contact c) {
        ContactSyncDTO dto = new ContactSyncDTO();
        dto.externalId = c.External_Id__c;
        dto.firstName = c.FirstName;
        dto.lastName = c.LastName;
        dto.email = c.Email;
        return dto;
    }
}
```

Usage:
```apex
List<ContactSyncDTO> payload = new List<ContactSyncDTO>();
for (Contact c : contacts) {
    payload.add(ContactSyncDTO.fromContact(c));
}
String body = JSON.serialize(payload);
```

## To Validate

- Confirm wrapper naming conventions (`*Wrapper`, `*DTO`) match the broader codebase.
- Ensure wrappers are not overused for simple cases where plain SObjects suffice.


