---
layout: default
title: Order of Execution
description: Understanding the order of execution in Salesforce is critical for architects and developers
permalink: /rag/development/architecture/event-driven-architecture.html' | relative_url }}">Event-Driven Architecture</a> - Async processing patterns

## Q&A

### Q: What is the difference between before-save and after-save automation?

**A**: **Before-save** automation runs before the record is saved to the database. You can modify field values, but cannot perform DML on other records. **After-save** automation runs after the record is saved. The record is read-only, but you can perform DML on other records and query related data.

### Q: When should I use before-save vs after-save flows?

**A**: Use **before-save** flows for field value modifications, simple validations, and calculations that need to be saved with the record. Use **after-save** flows for related record operations, complex validations requiring queries, rollup calculations, and operations that don't need to modify the current record.

### Q: What is the execution order of validation rules?

**A**: **System validation rules** execute first (step 3), before any automation. **Custom validation rules** execute during before-save (step 4), after before-save flows and triggers have run, so they can reference field values modified by before-save automation.

### Q: Can I modify field values in after-save automation?

**A**: No, records are **read-only** in after-save automation. You cannot modify field values in after-save flows or triggers. To modify field values, use before-save automation (before-save flows or before triggers).

### Q: What happens if multiple triggers exist for the same object?

**A**: If multiple triggers exist for the same object and event, there is **no guaranteed execution order**. Triggers execute in undefined order. Best practice: use one trigger per object per event type and use a trigger framework to manage trigger logic.

### Q: Can I perform DML operations in before-save automation?

**A**: No, **before-save automation cannot perform DML operations** on other records. You can only modify field values on the current record. To perform DML on other records, use after-save automation or async processing (Platform Events, Queueable, etc.).

### Q: How do I prevent trigger recursion?

**A**: Prevent trigger recursion by checking if field values have actually changed before performing updates, using static variables to track execution, implementing guard clauses, and avoiding update operations that would re-trigger the same trigger. Use trigger frameworks that handle recursion prevention.

### Q: What is the performance impact of before-save vs after-save automation?

**A**: **Before-save** runs synchronously and impacts user save time - keep it fast. **After-save** can be slower since the record is already saved, but complex operations in after-save can still impact overall transaction time. Move heavy operations to async processing (Platform Events, Queueable) when possible.

## References

- Salesforce Documentation: Order of Execution
- Trailhead: Apex Triggers and Order of Execution
- Best Practices: Understanding Salesforce Order of Execution

