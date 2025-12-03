# DevOps Center

**Source**: The Detail Department Confluence
**URL**: https://tddprojects.atlassian.net/wiki/spaces/SF

---

This is the start of the journey into DevOps Center, out now as a “free” tool (future enhancements may cost, but the basics will be included in your EE and above licencing).

I have been using the Pilot and so far the hardest thing has been typing Center rather than Centre. Why oh why oh why do they use US specific spelling to a global audience? The short form is DoCe.

Docs

Help Docs

Feedback

DevOps Center Group on Trailblazer Community

Articles and Videos

Salesforce DevOps Center: A Deeper Dive | Salesforce Ben

Video

#TDX22 DevOps Center  session.  Demo https://vimeo.com/709299094

No More Change Sets

Just say NO to Change Sets. Make it your mission to never use Change Sets again!

No Partial Sandboxes

Unfortunately Partial Sandboxes are just not for development. We can wish all we want but Salesforce is never going to make them useful. You can’t do source tracking on them, they will not sample the right data, and you don’t have enough control. This brings us to the issue of Sandbox Seeding and I am yet to find an excellent solution. I have tried Spanning Backup and Cloud Ally and neither worked with a relatively simple data structure. I know Snowfakery can do it with a lot of work.

You don’t need to be fancy with DevOps

Do NOT believe what other people are saying about DoCe:

You do NOT need to use Scratch Orgs

You do NOT need to have a full dev team and a documented CI/CD process

In fact, if you already do have a full CI/CD process then stick with it, DoCe is not for you.

You do NOT need to install any other add-in or paid app to make it work. There are apps that have been developed to work in conjunction with DoCe, but you don’t NEED them

You do NOT need to have a complex deployment process - just using it for Sandbox to Prod is completely fine. That is all I will be talking about on this page.

Work Item

DoCe starts with a Work Item - like a Ticket in Jira. Create a Work Item and then do your stuff, then get the changes associated with that Work Item, then deploy that Work Item. There is more to it than that but that is the basics. You can deploy multiple Work Items at once.

Unfortunately Work Item is not like a regular Custom Object so you can’t add Custom Fields to it so it can’t be used as a regular ticketing system. There is only a Title, a Description, and an Owner. It is so limiting. So just stick a URL into your Ticketing System into the Description.

Source Tracking

As you go through and make your changes in your (Developer) Sandbox, the changes will be tracked and you will pull those changes into DoCe, then deploy them to the linked org (eg Production). At the same time, and behind the scenes the changes will be committed to and saved in Github, which is very handy.

Changes can be made within the Sandbox or directly in SFDX and uploaded back to the Sandbox. DoCe will track those changes no matter where they are created.

Production

Yes, if you make changes in Prod you can reverse merge them back into your Sandbox. I have not tried this for real yet.

Set Up

Search for Dev Hub in your Production Org and Enabled Source Tracked Sandboxes and Enable Dev Hub

If you have a dev team that does fancy things with DevOps or DX check with your Dev team before enabling it in your Production Org, but it should be enabled anyway.

Open image-20220625-081410.png

Also ensure you have Github as DoCe will only work with Github at the start.

You can create free private repos in Github.

Ensure this is not your own Github account but one owned by your company. Even metadata should not be saved in a personal Github account.

Next, create or refresh a Developer Sandbox (not Partial). You must have a sandbox that has been created AFTER you enabled Source Tracking.

Search for DevOps Center in the setup, then enable it. Then click to install the package.

Open image-20220625-081052.png

After installing, DevOps Center is an app in your App Launcher.

Why is DoCe a package, and not a part of Salesforce? Well a few things seem to be heading this way now. It allows the product teams to release on a different schedule than the main 3 releases a year. That won’t necessarily mean more frequent releases but hopefully bug fixes can be done more easily. Even though it is a package, it will still get support. (In the beta, DoCe feedback is via the GitHub space here

GitHub - forcedotcom/devops-center-feedback).

The UI

Now, the first thing you notice when opening DoCe is that it opens in a new tab AND takes up the whole screen. (And just keeps your current screen open on the App Launcher). DoCe is a “builder” UI, like Lightning App Builder, Email Template Builder, and other “builders”. However the UI really sucks. It doesn’t look like the rest of Salesforce. How does a team even GET to build something that doesn’t follow Salesforce’s standard design blueprint. They have created a whole Design System, yet any team can come along and create any mess they like and call it Salesforce? This is why we need a Setup PM - there must be unity and cohesion in ALL setup screens.

Open image-20220625-085010.png

Whilst the data for Projects, Work Items etc is in your org there is no way to easily see it within your org. There is a tab for Projects, but it doesn’t show anything but the name. You could build out the page layouts and tabs for the other objects, but there really is no need. You can create Reports after you create Report Types.

Getting Set Up

New Project

A project is basically an org. You may only ever have one Project and that is OK.

Create a new Project

WTF is with the careless UI here - how does that even get past testing?

Open image-20220625-085303.png

Ignore the bits about DX Project Structure - that is just the way things are now… you won’t need to know about it unless you want to.

Create a Repository is the easiest.

You now have a Project record in DoCe and a Private empty Github Repo with the name you have chosen.

Note: You may want to be a lot more creative with your Repo names than I as it is just a Repo in your Github, and if it is mixed in with all your company’s other Repos you will need to know the naming convention you need to follow.

Open image-20220625-090137.png

Connect to Prod

Now you will connect your orgs. Starting with Production. Click Click to Connect.

You will notice that the UI just does NOT follow any Salesforce conventions. Normally in Salesforce an action on a row will be in a dropdown box at the end of the row.

Open image-20220625-092017.png

The default name was TDD Release, but I renamed it to be Prod to keep it simple, as we are only having Prod and Sandbox.

Log in and allow access to DevOps Center in the org.

It seems weird to do that, when this is the org that DoCe is already installed in.

Open image-20220625-092440.png

Now what do you do? there is no “action link” here now… So you have to click into the Project record to continue.

Connect to Sandbox

When you click into the Project, this is what you see… ignore all that for a bit and click Settings

Open image-20220625-092556.png

Click Add to add the Sandbox

Open image-20220625-092654.png

Make sure you have logged into your newly created Sandbox before doing this step, so you can set up the MFA and ensure everything is OK with the Sandbox.

Open image-20220625-092959.png

Again have a good naming convention here - probably similar to the name of the Sandbox.

At this step select “used for development” and choose Sandbox

NOTE: I had an issue here, I use Enhanced Domains and the login screen here only takes you to test dot salesforce dot com, so I had to hack the URL to enter my enhanced domain at the this step.

Open image-20220625-095023.png

Set up your Pipeline

We are going to simplify things here. I would love to see a wizard where it asks you what type of environments you work in, and sets this up as simple mode if you only use Sandbox and Prod.

Open image-20220625-095201.png

For Integration, UAT and Staging stages, click the drop down arrow and click Remove Stage

Now we have a simple setup, and can click Activate.

Ignore Bundling Stages and Branch Names as we are keeping it simple

Open image-20220625-095441.png

Work Items

Now we can create a Work Item

Open image-20220625-095545.png

Why is it that the New Work Item button doesn’t even look like a regular Salesforce button?

Open image-20220625-100128.png

WTF is wrong with the tab setting on the bulleted list. OMG.

Enter the details. As noted above, this is NOT a Jira ticket or a ticket in any way shape or form. Just put in a simple description and link to the ticket in your ticketing system of choice.

This is the thing that you are going to be doing next, and deploying. It may take a bit of trial and error to work out what is in a Work Item for you.

Build your Changes

Open image-20220625-100348.png

Now I don’t know if you have to set this first, before you make your changes in the Sandbox, but hopefully not. I think this should be a setting on the Project level and be set already at the Work Item level.

Click Proceed.

Open image-20220625-100500.png

Now the Github branch has been created. Again, don’t worry too much about this, all the Github stuff is seamless.

Now go ahead and build your things in your Sandbox.

Pull Changes

Now that you have built your items, click Pull Changes on the Work Item.

Note: You may have two Work Items on the go and ALL the changes will be pulled, but don’t worry you get to choose which Metadata components are related to this Work Item

Open image-20220625-102654.png

I created a Flow, created a custom field, added the field to two Page Layouts, added the Flow to a Lightning Page, gave perms to some Profiles for the new Field and added a Perm Set to handle the perms for people doing Account Management.

Note there is a component I added Manually in there.

Note that just because Profiles are pulled that does NOT mean we are going to start deploying Profiles. Do NOT deploy Profiles, no matter what deployment method you are using. Deploying Perm Sets is fine though.

Commit

Select the metadata components you are going to commit, enter a note, and then click Commit Changes

Open image-20220625-103137.png

Create Review

Now the next step is really weird. After you Commit Changes, the only thing that happens is that the Commit Changes button turns grey. So you have to know that the next step is to Create Review.

Click Create Review

You have to do this step for each Work Item

Open image-20220625-103500.png

Ready to Promote

You thought the last step was weird, this one is even weirder. Where in Salesforce have you ever seen a UI where you need to use a Toggle Button to move an item along in a stage?

Click Ready to Promote. All it does is change the stage to Ready to Promote and locks the Work Item from any further changes (you can toggle Ready to Promote off if you need to make changes though).

Open image-20220625-103826.png

Despite providing all this as feedback during the Pilot phase, nothing was done to improve this process.

Approve Work Items

Now go back to Pipeline (does it feel like this UX is just a bit strange? It is).

Open image-20220625-104111.png

This is where you can work on multiple Work Items and get them all to the Ready to Promote / Approved stage and then the next steps are done when you are ready to deploy your changes to Prod.

Promote

Choose the Work Items to Promote and click Promote Selected.

Open image-20220625-104243.png

Log into your Prod org

Open image-20220625-104337.png

Then after the screen refreshes about 5 times, you will need to go in and select your Work Items to Promote again, and choose Promote Selected again.

And this is again just so weird since you are already logged into Production (but remember it could be a completely different production org that you are deploying to. But it should be smart enough to work out that I am in this org and already logged in).

Open image-20220625-104520.png

Keep the defaults here.

Note: you may wan to change the test settings - this is the same as all other deployments you make to Production.

Click Promote - which should read Deploy, as it is now Deploying to Production!.

Deployment

Open image-20220625-110314.png

No Deployment Fish here, but whilst the deployment is at this stage, you can still go into your Deployment Status in your production org and watch it from there if you want.

Deployed

Open image-20220625-110437.png

Open image-20220625-110522.png

And that’s it, the Work Item is now Deployed!

Github

Behind the scenes Github has done a Pull Request for the commits and the Work Items you have made, and merged those items into the branch you selected at the beginning (eg Main).

Open image-20220625-111349.png

And you can see all the metadata of all the items you have deployed

Open image-20220625-111507.png

Work Items List Views

Now this list view is going to get bigger and bigger and bigger with all your closed Work Items and there is no way to create List Views like you would in regular Salesforce. So you will have to use the Filter each time you go in here. At least you can sort in reverse date order though.

You could create a Tab for Work Items and you could even create Custom Fields for Work Items, and treat them as any Salesforce records, but you can not see any of that additional information in DoCe, so what is the point?

Open image-20220625-111052.png

Deployment Errors

From here on in the Deployment is exactly the same as a regular Salesforce Deployment and has all the same foibles.

Open image-20220625-104805.png

Click to view the details

Open image-20220625-104850.png

Click Error Details

Open image-20220625-104924.png

The error details here are exactly the same error details you will get in Deployment Status in your org. (eg just as unintelligible).

But it’s easier to read in Deployment Status

Open image-20220625-105140.png

So I need to fix my Account Page Layout and Account Lightning Page.

Then I needed to go back into my Work Item, un-toggle Ready to Promote, pull my changes, then commit them and put it back to Ready to Promote and go back into the Pipeline to Promote / Deploy again.

Add Components Manually

Open image-20220625-101001.png

You can add Components Manually which is a nice new feature since the pilot. To do this you need to fully understand your Metadata, which I encourage you to learn more about, but you don’t need to do this step - you can rely on the Source Tracking.

It is interesting that it is a nicer UI than Change Sets but does not have any of the related Metadata Search that is built into Change Sets already and could easily be added to this UI. Such a miss.

You can’t REMOVE Components after you add them, but you can just not select them to be committed for this Work Item.

Changes in Prod

You are meant to be able to sync your Dev Org with changes made in Prod. Do this rather than refreshing your sandbox too often (don’t refresh while Work Items are in progress).

Open image-20220625-113231.png

Open image-20220625-113244.png

However it did not seem to work. I will have to try it again.

Open image-20220625-113415.png

Tips

Start SLOW! Just go from one Sandbox to Production and get used to that.

Then work with your Dev team to work out the “pipeline” and how Sandboxes will be managed.

You can use your DevOps centre in one org and use it to deploy to and from completely different orgs. So me as a Partner, I install it in my Partner Org and can have one central place for all the deployment of all my client’s orgs. As it’s not data, it’s just metadata, I don’t have a problem in keeping them all together. I have previously kept the metadata of all my client orgs in Bitbucket for backup.

Advanced Features

You may want to get all your org’s metadata into Github first, so you can see the changes to your org as you deploy things. See

Getting started with Salesforce DX – Salesforce Developer Experience for more info on how to get all your Metadata.