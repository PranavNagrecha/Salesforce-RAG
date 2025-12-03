# Data Migration Code Examples

> Complete, working code examples for data migration patterns.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

Data migration involves importing, transforming, and validating data in Salesforce. These examples cover common migration scenarios and patterns.

**Related Patterns**:
- [Data Migration Patterns](/rag/data-modeling/data-migration-patterns.html)

## Examples

### Example 1: Data Import with Validation

**Pattern**: Importing data with validation and error handling
**Use Case**: Bulk data import with validation
**Complexity**: Intermediate

**Solution**:

```apex
/**
 * Service class for data migration with validation
 */
public class DataMigrationService {
    
    /**
     * Import contacts with validation
     * @param contacts List of contacts to import
     * @return MigrationResult with success and error counts
     */
    public static MigrationResult importContacts(List<Contact> contacts) {
        MigrationResult result = new MigrationResult();
        List<Contact> validContacts = new List<Contact>();
        List<MigrationError> errors = new List<MigrationError>();
        
        // Validate each contact
        for (Integer i = 0; i < contacts.size(); i++) {
            Contact contact = contacts[i];
            List<String> validationErrors = validateContact(contact);
            
            if (validationErrors.isEmpty()) {
                validContacts.add(contact);
            } else {
                errors.add(new MigrationError(i, contact, validationErrors));
            }
        }
        
        // Import valid contacts
        if (!validContacts.isEmpty()) {
            Database.SaveResult[] saveResults = Database.insert(validContacts, false);
            
            // Process results
            for (Integer i = 0; i < saveResults.size(); i++) {
                if (saveResults[i].isSuccess()) {
                    result.successCount++;
                } else {
                    result.errorCount++;
                    errors.add(new MigrationError(
                        i,
                        validContacts[i],
                        getErrorMessages(saveResults[i].getErrors())
                    ));
                }
            }
        }
        
        result.errors = errors;
        return result;
    }
    
    private static List<String> validateContact(Contact contact) {
        List<String> errors = new List<String>();
        
        if (String.isBlank(contact.LastName)) {
            errors.add('Last Name is required');
        }
        
        if (String.isNotBlank(contact.Email) && !contact.Email.contains('@')) {
            errors.add('Invalid email format');
        }
        
        return errors;
    }
    
    private static List<String> getErrorMessages(List<Database.Error> dbErrors) {
        List<String> messages = new List<String>();
        for (Database.Error error : dbErrors) {
            messages.add(error.getMessage());
        }
        return messages;
    }
    
    public class MigrationResult {
        public Integer successCount = 0;
        public Integer errorCount = 0;
        public List<MigrationError> errors = new List<MigrationError>();
    }
    
    public class MigrationError {
        public Integer rowNumber;
        public Contact contact;
        public List<String> errorMessages;
        
        public MigrationError(Integer rowNumber, Contact contact, List<String> errorMessages) {
            this.rowNumber = rowNumber;
            this.contact = contact;
            this.errorMessages = errorMessages;
        }
    }
}
```

**Explanation**:
- Validates data before import
- Handles errors gracefully
- Returns detailed results
- Continues processing valid records

---

## Related Patterns

- [Data Migration Patterns](/rag/data-modeling/data-migration-patterns.html) - Complete migration guide

