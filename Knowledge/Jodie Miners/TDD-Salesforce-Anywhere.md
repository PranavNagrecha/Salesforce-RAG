# Salesforce Anywhere

**Source**: The Detail Department Confluence
**URL**: https://tddprojects.atlassian.net/wiki/spaces/SF

---

Salesforce Anywhere Glitches

Why Salesforce Anywhere

Ah, such a great concept, there were so many cool things about this, but it has GONE! There was something else called Salesforce Anywhere, but it was what Quip was renamed to for a second. But now Quip.com’s contact page just goes to Slack.

What is it? Why do I want it? What is available now? How do I set it up?

Answer: who knows… let’s try to find out.

NOTE: Salesforce Anywhere is a “Non-GA Service”. What does that mean? Well who actually knows. And there is even more scary words saying it’s “subject to the terms and conditions of the Universal Pilot Research Agreement ("UPRA"), including the Data Processing Addendum to the UPRA”. “Use of this Non-GA Service is at your sole discretion”

All that sounds really scary and it sounds like your data is not safe using this feature. I don’t know that but that is what it sounds like. Please be cautious using this feature.

From Release Notes.

Pricing

How much will this be? Who knows?

An interesting tidbit in the chatter group “neither org file nor data storage will be consumed by Salesforce Anywhere usage”. So they have to make money somewhere… this will be interesting. I wonder if it will be tiered usage. Like I would expect Chat and the “live record” feature (that is not really know anything about yet, but hopefully is the reincarnation of cache invalidation) is both included in your licence. I can understand having to pay for Zoom integration on top of Zoom licencing though.

Help Docs

This is all the docs I could find for now https://help.salesforce.com/articleView?id=rn_anywhere_july_2020.htm&type=5 and this Quip doc about the sandbox access setup https://thedetaildept.quip.com/gG6vANba9bta/Set-up-Salesforce-Anywhere-in-Sandbox

Setting up

First you have to have registered for the beta. Then you have to wait for it to be given access. A popup will appear in your org when it is there. (It is there for one org but not another).

Then you go to Salesforce Anywhere under Feature Activation in Setup. There is a screen to guide you through the steps.

Oh so you have to click the link that says + Disabled to turn it on. Now I can’t do that in a client’s org and I can’t suggest to a client they turn it on until I know what it’s all about. So back to waiting until I get access to it in my org.

Ok so I refreshed a sandbox and can try it from there.

Legals

Open image-20200730-052822.png

Why does this say Beta, when the Release Notes says Non-GA Service? The help docs says Beta also.

Why do some orgs get it enabled automatically and some have to sign extra legal agreements to get it activated?

Why doesn’t this say what it says in the release notes… “Use of this Non-GA Service is at your sole discretion”.

Permissions

So it says “Specify who can use Salesforce Anywhere in Lightning” and a button to Set Permissions, but no notice of what permissions are required. It’s not a permission set licence. This help doc just says they have to be Salesforce Platform or Lightning Platform users. But here it says “When you turn on Salesforce Anywhere, permission sets are automatically created. By default, Salesforce Anywhere on mobile is enabled for all users, and Salesforce Anywhere in Lightning Experience is disabled for all users”.

Permission Sets

“When you turn on Salesforce Anywhere, permission sets are automatically created. By default, Salesforce Anywhere on mobile is enabled for all users, and Salesforce Anywhere in Lightning Experience is disabled for all users”.

“To change the Salesforce Anywhere experiences users can use, click Set Permissions next to the permission set you want to assign to or remove from users.”

They still don’t tell you which Permission sets to assign or remove.

The only action in the Audit Log is “Organization setup action: isotopeEnabledOffOn has changed.” If this happens you need to contact Salesforce via the Chatter group to get them to nudge the creation of the permission sets.

Open image-20200730-050741.png

Open image-20200730-050627.png

Salesforce Anywhere in Lightning Experience

So this shows us why it didn’t work when creating it manually. It needs the External Data Source access. It also granted access to Files Connect as the Data Source is a Files Connect data source.

From the Audit Trail

Created a new Files Connect: Salesforce Anywhere external data source: Salesforce Anywhere

Permission Set in VS Code

<PermissionSet xmlns="http://soap.sforce.com/2006/04/metadata">

<description>Use Salesforce Anywhere in Lightning Experience.</description>

<externalDataSourceAccesses>

<enabled>true</enabled>

<externalDataSource>SalesforceAnywhere</externalDataSource>

</externalDataSourceAccesses>

<hasActivationRequired>false</hasActivationRequired>

<label>Access to Salesforce Anywhere in Lightning Experience</label>

<userPermissions>

<enabled>true</enabled>

<name>ContentHubUser</name>

</userPermissions>

<userPermissions>

<enabled>true</enabled>

<name>IsotopeLEX</name>

</userPermissions>

</PermissionSet>

Salesforce Anywhere on Mobile

I’m not sure why this one did not work manually?

<?xml version="1.0" encoding="UTF-8"?>

<PermissionSet xmlns="http://soap.sforce.com/2006/04/metadata">

<description>Use the Salesforce Anywhere mobile app. Initially assigned to all users by default.</description>

<hasActivationRequired>false</hasActivationRequired>

<label>Access to Salesforce Anywhere on Mobile</label>

<userPermissions>

<enabled>true</enabled>

<name>IsotopeAccess</name>

</userPermissions>

</PermissionSet>

Salesforce Anywhere Integration Object and User

The permission set named “Allow Salesforce Anywhere Integration Object Access” and “Gives the Salesforce Anywhere Integration user Read and View All Records permissions on Salesforce objects. Allows for administrator control over access to objects. Do not assign to users.” At least that is clear.

However you can’t even assign that permission set to a user.

OK, so setup Audit trail tells us there is a Platform Integration User (and shows the User ID) and then shows “Permission set Allow Salesforce Anywhere Integration Object Access”. That user is NOT in your list of users and that assignment is NOT shown against the permission set. I would copy that User ID so you can see later what that user is doing.

And weirdly it does Not just give Modify All to that user, it gives View All and Read to many objects via the Permission Set. So if you add a new object, then you need to modify this permission set. Note that it is granting to managed package objects also. BEWARE if you have something like FinancialForce with so many objects that you don’t know what they do.

This is an example of the permissions granted. Just Read on every object.

<objectPermissions>

<allowCreate>false</allowCreate>

<allowDelete>false</allowDelete>

<allowEdit>false</allowEdit>

<allowRead>true</allowRead>

<modifyAllRecords>false</modifyAllRecords>

<object>Case</object>

<viewAllRecords>true</viewAllRecords>

</objectPermissions>

Quip

So do I NEED Quip? Dunno.

So this is the first sign of Quip. From here:

WOW beware of this one!

”When you add users and grant them access to use Salesforce Anywhere, they can connect and their account gets configured automatically. But when a user is deactivated or frozen in your Salesforce org, we suggest disabling the user account via the Quip Admin Console.”

So a user will continue getting updates to all data even though their user has been deactivated in Salesforce? No that is not good at all. (Now maybe there is something in Session Activation that will prevent this because the permission set for the integration user has session activation required. Please test this before you launch!)

And from here, if you already have a Quip site you can grant access to users from your Salesforce org.

Setting it up still

I have activated it but still don’t see anything.

In the Send a Welcome Email button there is a hint. (yes with raw HTML thrown in as a bonus)

In Salesforce Lightning: Start a chat using any of these methods:

At the top of your browser, use the Salesforce Anywhere icon to open your chat inbox.

Hover over a person’s name and click <strong>Message</strong> to send someone a direct message

From a record page, click Share In Chat.

So, I have no Salesforce Anywhere Icon. Where exactly do I hover over a person’s name - is that a User? I go to the user detail and there is no message there. I hover over the name in chatter and there is no message button. When you have the permissions assigned to the user there is a Message button on the User detail. I do not know what the hover over a person’s name means though.

Open image-20200730-052349.png

There is a hint in the help documents that references the Salesforce Anywhere Component. There is no Component in the Home Page. There is no Component in the Record Page.  Maybe it’s the Quip components? Not sure.

There is some inkling in the chatter group that things aren’t going smoothly. I have tried to disable and will re-enable it. But it does say that the appropriate Permission Sets SHOULD be created.

Ah so now I get a Share in Chat button on a record but it just says “Please complete authentication with Salesforce Anywhere by clicking the Salesforce Anywhere header button.”

After a week I got the permission sets created automatically. Now I have the chat button. But then I get the dreaded JSON error. Back to asking for manual help to get this set up.

Issues

Mind the Gap! Why? How? It’s actually technically correct, but it just looks really bad. The question mark icon just has extra white space around the icon itself. They could still fix it though by having less padding to the right of the chat icon.

Open image-20200730-044340.png

Also why the icon change? It used to be the direction arrows. At least one help topic still has the direction arrows.

Use Cases

From here. OMG does Salesforce have any OTHER use-cases than confetti? “Deal celebration: Send a celebratory message to a sales team group chat when an opportunity closes.”

What is the Group Chat feature - we haven’t seen anything in the help notes yet about groups?

Using the App

Salesforce Anywhere Glitches

Why Salesforce Anywhere

Steps

Register for the Beta

Wait for activation. Or in some cases (don’t know why) you just get it activated.

Click + Disabled in Salesforce Anywhere Feature Activation.

Hopefully permission sets will be created (if not ask in the chatter group)

Assign the Lightning Permission Set.

Refresh Salesforce. The chat icon should be in the header.

Go to a record. See “Share in Chat button”

Click it

Get error message.

Sign into incognito window and then click the chat icon in the header. (This is because I have a Quip in a different user name that already has cookies in this browser)

Behind the scenes a new Quip chat instance is created.

After that is set up click Chat in the header.

Get error in Incognito mode.

Now go back to regular window and try again.

Click New Chat

Type in the name of a user who is also already set up in Chat and click send.

A chat is sent!

Try to log onto the mobile app on iOS

Get a Quip error.

Update iOS to the latest version.

Finally be able to log in.