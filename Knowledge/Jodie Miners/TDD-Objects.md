# Objects

**Source**: The Detail Department Confluence
**URL**: https://tddprojects.atlassian.net/wiki/spaces/SF

---

Details

Rules

All Contacts must belong to an Organisation - never allow private Contacts.

Never sync Contacts from Outlook or Google Contacts - have rules on how Contacts are created. Use Lightning Sync to sync TO Google or Outlook if you need to.

If you "must" have info@ email addresses for organisations, create a contact for each org named Generic Contact so you can a) spot them, and try to eradicate them and b) add them to campaigns. Mailchimp and Campaign Monitor will NOT send emails to generic email addresses.

Have a good Dupeblocker app or set up standard Salesforce Duplicate Management as the bare minimum.

New Salesforce Org

Setup

Display Middle Name and Suffix fields in User Interface if you are going to need those fields - don't create your own.

Definitely do this if you are doing legal contracts.

Fields

Rename Title to Position or Job Title to not confuse it with Mr, Mrs etc.

Rename all State/Province names to State

Rename all Zip/Postal names to Post Code

Rename Other Address to Physical Address to keep it similar to Accounts.

Rename City to Suburb

New Fields

Data Source - for where the record came from

Data Cleansing - for quickly marking any notes for bulk data fixes.

Preferred Name - especially when you need their full name for legal contractual reasons.

City State Country

Ultimate Parent

Campaign Monitor Fields

Permissions

Set permissions on the following fields that are not read or edit by default:

Do Not Call

Email Opt Out

Fax (if used)

Birthdate (only if needed)

Description

Informal Name (nope, you can't. Vote for this Idea).

Search Layouts

Ensure you set up your Search Layouts

Buttons Links Actions

Remove Mail Merge buttons

Remove Request Update

Make Email the first button in Lightning buttons

Don't add Note unless your company has made an executive decision to use and support notes.

Remove Printable View unless your staff have a definite need to print things. Do NOT encourage people to print data. Also, it's very ugly.

OR Upgrade to Dynamic Actions instead of managing on the page layouts. (Same buttons though).

Open image2018-2-26_15-56-23.png

Layout

Hide Birthdate or add it only to particular Record Types (Add fields for birth day and month is really needed. There should not be a reason to collect Birthdate - or maybe add it to the new Individual Object for GDPR Compliance).

Hide Assistant and Assistant Phone because if they are that important they should be separate contacts, and who really has assistants these days?

Add Do Not Call

Add Email Opt Out

Only include one address field - or lay out the address fields above one another rather than side by side because with State and Country Picklists as they are impossible to edit if you use the Edit button. (I haven't used State and Country Picklists in a while as I find them to be more of an issue than they are worth, but useful if you are still doing mailings).

Only have one Page Layout for Contacts unless you store a heap of data on Contacts!

Note, I always put Owner in the top right hand corner of the Page Layout, and Record Type in the top left. But if they are on the Highlights panel it may be superfluous. So you may put them in System Fields... but anyone that has moved from Classic can never find it in the Highlights panel

Views

See Views

Apps

Use a Salesforce Side Panel app in Gmail or Outlook - eg Cirrus Insight or Lightning for Outlook and Lightning for Gmail.

Lightning Page

See also Record Page for details on setting up Lightning Record Pages.

Open image2022-8-29_17-40-27.png

Notes:

Header

2 buttons only shown - show all the New Record buttons then Edit - the rest of the buttons including Delete and Clone are under the dropdown. Upgrade to Dynamic Actions.

Compact layout shows RecordType (if applicable) and Owner.

Account Name (or the Parent Field) is ALWAYS the first column shown on the Compact Layout.

Left Column

Details Tab

Related List Quick Links at the top (you may delete this if there are not many related lists or far too many related lists, it becomes overwhelming if you can't find things easily).

Set the order of Related Lists on the Page Layout

Remove Notes and Attachments, add Files (See Files, Content, Attachments, Documents etc. You may still want Notes and Attachments if you have an old org that is not feasible to move to Notes).

Related Tab only with Dynamic Related List - Single or Related List - Single components, and only show the lists that you need.

Conditional Related Record Components or Related Lists only for key details for key staff. Eg if Marketing Staff ALWAYS need to see Campaigns details related to Contacts then put that at the top of Details and make it visible only to them.

Details Component

Include Addresses stacked rather than side by side if using State and Country picklists as they are impossible to edit if you use the Edit button

Then conditional Related Record Components - these are only available to System Admins. See Actions! Global and Quick Actions for details

Other tabs for key details, charts or other Actions as required.

Eg I often put a Key Details RR Component on the first tab, with a few key Related Lists, then put the Details Component on the second tab. It really depends if people are editing often or just looking at key data often.

Right Column

Indicators can be displayed first. See Actions Examples for more ideas.

Duplicates displayed front and centre and always in the same place as Accounts.

Then key Related Record Components such as Parent, since our hover details are so compromised now with only being able to see 4 fields as defined in the compact Layouts.

Chatter tab first. Actions Tab second. See Action Views, Tasks and Report Alerts for why!

Only a very few really important components should be displayed before Chatter.

Files (and / or Notes) below Chatter if you are going to use them extensively for Contacts.  (Use Chatter Scrollbar AppExchange Component if your Chatter gets too long).

Person Accounts

I don't HATE Person Accounts with a passion like others do, but I do much prefer the NPSP's way of handling individuals in Salesforce, than Person Accounts.

Story about Person Accounts and Workflows (old now, and I haven't seen if it is the same for Flows, it probably is).

Click here to see the story...

See Articles

Page:

Working with Person Accounts in Salesforce.com