---
layout: default
title: DML Mocking Patterns
description: Patterns for testing Apex logic that performs DML without relying on real database writes
permalink: /rag/testing/dml-mocking-patterns.html
---

## What Was Actually Done

- Used dependency injection to separate business logic from DML persistence, enabling tests to replace DML with in-memory mocks.
- Created small repository interfaces (e.g., `IContactRepository`) that encapsulate `insert`, `update`, and `delete` operations.
- Implemented test repositories that record requested operations without committing to the database.

## Patterns

### Pattern 1: Repository Interface for DML

```apex
public interface IContactRepository {
    void insertContacts(List<Contact> contacts);
    void updateContacts(List<Contact> contacts);
}

public with sharing class ContactRepository implements IContactRepository {
    public void insertContacts(List<Contact> contacts) {
        insert contacts;
    }
    public void updateContacts(List<Contact> contacts) {
        update contacts;
    }
}
```

### Pattern 2: Service Depending on Repository

```apex
public with sharing class ContactService {
    IContactRepository repo;

    public ContactService(IContactRepository repo) {
        this.repo = repo;
    }

    public void processContacts(List<Contact> contacts) {
        // validate and transform
        repo.insertContacts(contacts);
    }
}
```

### Pattern 3: In-Memory Mock Repository

```apex
@IsTest
private class InMemoryContactRepository implements IContactRepository {
    public List<Contact> inserted = new List<Contact>();
    public List<Contact> updated = new List<Contact>();

    public void insertContacts(List<Contact> contacts) {
        inserted.addAll(contacts);
    }
    public void updateContacts(List<Contact> contacts) {
        updated.addAll(contacts);
    }
}
```

Usage in test:
```apex
@IsTest
private class ContactServiceDmlMockTests {
    @IsTest
    static void testProcessContacts_UsesRepository() {
        InMemoryContactRepository mockRepo = new InMemoryContactRepository();
        ContactService service = new ContactService(mockRepo);

        List<Contact> contacts = new List<Contact>{
            new Contact(LastName = 'Test')
        };

        service.processContacts(contacts);

        System.assertEquals(1, mockRepo.inserted.size());
    }
}
```

## To Validate

- Ensure repository-based patterns are only used where testability benefits justify the extra abstraction.


