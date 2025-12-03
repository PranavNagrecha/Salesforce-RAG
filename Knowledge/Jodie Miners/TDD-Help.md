# Help

**Source**: The Detail Department Confluence
**URL**: https://tddprojects.atlassian.net/wiki/spaces/SF

---

Help documentation for your Salesforce implementation is very important. How you will do it depends on your time, your skills and your budget.

Revisiting this for Lightning and expanding it to on page and full help text.

Video

Table of Contents

Validation Options

Before Save Flows

See this post and note the “considerations”.

I think it’s far too limiting as there needs to be a separate field for each error message needed.

this post is a little more involved and deals with picklist values

Alert Options

Custom Field with Emoji or Images

Rich Text Component

My

Indicators Lightning Web Component

This option - it’s a bit heavy handed though and just say NO to GIFs!

Lightning Messaging Utility (Salesforce Labs) - can do quite a lot (Docs) and was just featured on an article by the Labs team showcasing 15 new Labs Apps

Alert Message on any object (CloudRebelz) - simple (Docs)

I can’t find this app anywhere now, even as the new name of CT Consulting Alert Message. Very sad as it is really good.

Notifie - very basic (Docs)

PopUps - very comprehensive (Docs)

Help Snippets Options

Link to documents eg in Google Docs, SharePoint, Teams, Quip

In-App Guidance - only for short term notifications.

You can’t make in-app guidance display because of field values.

You can’t create in-app guidance for a specific record type or globally.

You can’t add Lightning Components to in-app guidance.

A user can’t reopen a prompt on demand. Instead, the prompt can appear more than once to ensure that the user acknowledges the content. This is the biggest limitation that makes it not suitable for a help system.

You can’t add in-app guidance to windows (such as Add Record), related lists, the Setup app, or Communities.

In-app guidance doesn't appear in the Salesforce mobile app.

From this knowledge base article

Flow - can be a little slow, can bog down the page a bit.

Helpful Links Component

Winter '21 Launchpad Component

Utility Bar Rich Text Component

Pop Ups

Guide Me (not particularly useful).

Tips (good enough for Free, but there is some paid options also - eg Videos is a paid option. US$1000 per year so pretty pricey).

Help Documents Options

Basic Salesforce Help documents.

Link to custom help documents in the top right hand corner

You could link to the Tip Sheets.

Or of course there is Trailhead. But sometimes Trailhead is not good for general users, it is better for people learning how to administer Salesforce.

Create your own Visualforce pages for Object Level Help. (Classic Only)

Or use this trick to show standard help text on custom Visualforce pages.

This option is for LWCs and this stackexchange post gives a nice complex example.

Create your own HTML pages

And save them as a Static Resource, and create a custom tab to access it.

Works really well, but the HTML files have to be very small.

I use Screen Steps to create the HTML files.

This works in Lightning too! I still like this option.

Or just create a Web Tab with a link to a Google Doc or SharePoint for a quick and easy option.

Box Lightning Component - a really nice lightweight option.

Spekit is now free for 10 users. But if you go over 10 users you have to pay for the first 10 first. It is difficult to get set up and even after setting it up I can’t get it to work well. Their demo video is impressive. If you have a resource who’s job it is to do help documentation then this might be useful.

Salesforce Knowledge - Hard work. Knowledge creators need to have a Knowledge licence which is paid. But you could then use this component to embed knowledge articles in pages.

Quip - yeah, Quip is lovely but you need the full version that integrates with Salesforce and that is just exy.

Not Free

Set up your own Confluence instance. US$10 per month for 10 users.

In-App Guidance Walkthroughs - requires a myTrailhead licence for each user US$25/u/m - not worth it.

Other

Other Apps not recommended

Service Agent Script for Lightning Flow - just build it yourself.

Crowd Guide from Train the Crowd - Classic Only still.

Tipster - Looks ugly. Does not look like Salesforce.

Screen Steps - has unfortunately priced itself out of the reasonable pricing realm now https://www.screensteps.com/pricing

Elements Cloud - Too Expensive, too time consuming, too opinionated.

Announcements Viewer (Salesforce Labs) - No docs, looks ugly

Headlines Marquee - No, I will not unleash that on anyone.

Also see

My blog post on Tools to Write Help Documents, including links to some examples of good and bad help systems. It's a bit old now, but there might be some good things in there.

My blog post on Training Resources for NFP Users on Salesforce.

Alice from Train The Crowd's Slideshare Building Help and Training to Make Every User an Expert.

The Resources page with links on how to get help for using Salesforce (again may be a bit out of date).

Examples of good help docs

https://documentor.in/2148/best-examples-product-documentation-guides/

Xero Central

Write the Docs

Lightning Design System

Technical docs examples

GitHub - matheusfelipeog/beautiful-docs: Pointers to useful, well-written, and otherwise beautiful documentation.

Trailhead on writing and writing for myTrailhead