---
layout: default
title: Trigger Framework Patterns
description: Patterns for implementing a single-trigger-per-object framework with handlers and domain classes
permalink: /rag/development/trigger-framework-patterns.html
---

## What Was Actually Done

- Implemented a single trigger per object that delegates to a handler class.
- Used handler methods for each trigger context (before insert, before update, after insert, after update, etc.).
- Combined the handler pattern with Domain and Selector layers to keep triggers lightweight and bulkified.

## Patterns

### Pattern 1: Single Trigger Delegating to Handler

**Trigger**:
```apex
trigger ContactTrigger on Contact (
    before insert, before update,
    after insert, after update
) {
    ContactTriggerHandler.run(Trigger.new, Trigger.oldMap, Trigger.isBefore, Trigger.isInsert);
}
```

**Handler Skeleton**:
```apex
public with sharing class ContactTriggerHandler {
    public static void run(
        List<Contact> newList,
        Map<Id, Contact> oldMap,
        Boolean isBefore,
        Boolean isInsert
    ) {
        if (isBefore && isInsert) {
            handleBeforeInsert(newList);
        } else if (isBefore && !isInsert) {
            handleBeforeUpdate(newList, oldMap);
        } else if (!isBefore && isInsert) {
            handleAfterInsert(newList);
        } else if (!isBefore && !isInsert) {
            handleAfterUpdate(newList, oldMap);
        }
    }
}
```

## To Validate

- Confirm all triggers in the org follow a single-trigger-per-object rule and delegate to handlers.
- Ensure handler methods are bulkified and do not contain SOQL/DML in loops.


