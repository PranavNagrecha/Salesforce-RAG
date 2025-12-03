# Rules for Fields

**Source**: The Detail Department Confluence
**URL**: https://tddprojects.atlassian.net/wiki/spaces/SF

---

Fields

All custom fields have help text.

If necessary, add help text to standard fields.

Unless otherwise noted Text fields are 255 characters in length.

Naming Things

No Underscores in Names

This is a bugbear of mine, and I don't care how anyone else does it, these are my rules! No underscores in API Names. Yes - type the name My Field Name in the name field, it will default to My_Field_Name in the API name, then go and REMOVE those underscores! The API Name will be MyFieldName__c. Thankfully there is a fabulous Chrome extension called Boostr that will do this for you - but be careful when changing labels as it will try to change the API Name also.

On a recent Good Day Sir Podcast (I think it was No. 98), John and Jeremy both said they had given up the fight and go with underscores now. NO! I'm still fighting!

Shorten names - eg Number to Num, but change No. to Num in the field name rather than just No in the api name.

Help Text and Descriptions

Always add Help Text - ALWAYS!

Add a description to anything that is added for a specific reason - eg a formula field for reporting.

Changing Names of Standard Objects

If the client changes the name of a standard object, all field names should have the API name to still refer to the standard object. Eg they change Case to be Complaint. They want a field called Complaint File Number. The API Name should be CaseFileNo__c. This is so if they decide, as they should, that Complaint is too restrictive, and they want to change the name to be something else, the API names don't need to change.

This is also the same for related objects to standard objects - eg Complaint References as the custom object - the API Name would be CaseReference__c.

Singular Object Names

Yes, object names should be singular, as shown in the above example.

Visibility

You DO NOT have to add fields to page layouts - see Grey Tab or Salesforce Inspector in Useful Google Chrome Extensions for Salesforce for a way of seeing the data without it being on a page layout.