---
layout: default
title: Apex Interface Patterns
description: Patterns and examples for using Apex interfaces to decouple implementations, enable mocking, and improve testability
permalink: /rag/development/apex-interfaces-patterns.html
---

## What Was Actually Done

- Used Apex interfaces to abstract data access (e.g., `IContactSelector`, `IAccountSelector`) so service classes depend on contracts instead of concrete implementations.
- Defined interfaces for external integrations (e.g., `IExternalNotificationService`, `IPaymentGatewayClient`) to allow swapping real/mocked implementations.
- Implemented test-specific classes that implement the same interfaces to avoid `SeeAllData` and enable deterministic tests.
- Used interfaces to isolate complex calculations and business rules so they could be reused from Flows, triggers, and LWCs.

## Patterns

### Pattern 1: Selector Interface

**When to use**: You need reusable, testable SOQL queries that can be swapped or mocked.

**Interface**:
```apex
public interface IContactSelector {
    List<Contact> selectByAccountIds(Set<Id> accountIds);
}
```

**Implementation**:
```apex
public with sharing class ContactSelector implements IContactSelector {
    public List<Contact> selectByAccountIds(Set<Id> accountIds) {
        if (accountIds.isEmpty()) {
            return new List<Contact>();
        }
        return [
            SELECT Id, FirstName, LastName, AccountId
            FROM Contact
            WHERE AccountId IN :accountIds
        ];
    }
}
```

**Test Double**:
```apex
@IsTest
private class ContactSelectorStub implements IContactSelector {
    private List<Contact> contacts;

    ContactSelectorStub(List<Contact> contacts) {
        this.contacts = contacts.deepClone(true, true, true);
    }

    public List<Contact> selectByAccountIds(Set<Id> accountIds) {
        return contacts;
    }
}
```

### Pattern 2: Service Interface for External Integrations

**When to use**: You call external services and need to swap callout vs. mock implementations.

**Interface**:
```apex
public interface INotificationService {
    void sendNotification(String recipient, String message);
}
```

**Production Implementation**:
```apex
public with sharing class HttpNotificationService implements INotificationService {
    public void sendNotification(String recipient, String message) {
        // Uses Named Credentials and HttpCalloutMock-safe design
        // See integration-examples for callout patterns
    }
}
```

**Test Implementation**:
```apex
@IsTest
private class InMemoryNotificationService implements INotificationService {
    public List<String> recipients = new List<String>();
    public List<String> messages = new List<String>();

    public void sendNotification(String recipient, String message) {
        recipients.add(recipient);
        messages.add(message);
    }
}
```

### Pattern 3: Factory for Interface Implementations

Use a small factory to choose the concrete implementation, which you can override in tests.

```apex
public with sharing class ServiceFactory {
    @TestVisible
    private static INotificationService notificationServiceOverride;

    public static INotificationService getNotificationService() {
        if (notificationServiceOverride != null) {
            return notificationServiceOverride;
        }
        return new HttpNotificationService();
    }
}
```

In tests:
```apex
@IsTest
private class NotificationServiceTests {
    @IsTest
    static void testNotificationsAreSent() {
        InMemoryNotificationService mock = new InMemoryNotificationService();
        ServiceFactory.notificationServiceOverride = mock;

        // Exercise code that calls ServiceFactory.getNotificationService()

        System.assertEquals(1, mock.recipients.size());
    }
}
```

## To Validate

- Confirm interface naming conventions match the broader codebase (e.g., `IContactSelector` vs `ContactSelectorInterface`).


