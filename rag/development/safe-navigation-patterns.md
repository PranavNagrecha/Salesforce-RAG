---
layout: default
title: Safe Navigation Patterns
description: Patterns for safely navigating nested relationships and avoiding null dereference errors in Apex
permalink: /rag/development/safe-navigation-patterns.html
---

## What Was Actually Done

- Centralized null checks when traversing relationships (e.g., `contact.Account.Owner`) to reduce `NullPointerException` risk.
- Used guard clauses and helper methods to keep business logic readable while handling nulls.
- Where supported, used the safe navigation operator (`?.`) to simplify deep property access in Apex.

## Patterns

### Pattern 1: Traditional Null Guard

**When to use**: Safe navigation operator is not available or you want explicit control.

```apex
public with sharing class ContactHelper {
    public static String getAccountName(Contact c) {
        if (c == null || c.Account == null) {
            return null;
        }
        return c.Account.Name;
    }
}
```

### Pattern 2: Safe Navigation Operator

**When to use**: Your org supports the safe navigation (`?.`) operator.

```apex
String accountName = contact?.Account?.Name;
String ownerEmail  = contact?.Account?.Owner?.Email;
```

This avoids `NullPointerException` if any intermediate relationship is null.

### Pattern 3: Helper Methods for Deep Access

Encapsulate repeated patterns for deep navigation.

```apex
public with sharing class RelationshipHelper {
    public static User getAccountOwner(Contact c) {
        return c?.Account?.Owner;
    }

    public static String getAccountOwnerEmail(Contact c) {
        return c?.Account?.Owner?.Email;
    }
}
```

## To Validate

- Confirm whether the safe navigation operator is enabled in the target runtime.
- Ensure tests cover both populated and null relationship scenarios.


