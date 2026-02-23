PROMPTS = {

 "FEED_SCROLL": """
You are an intelligent browser automation agent simulating realistic human LinkedIn browsing behavior.

========================================
OBJECTIVE
========================================
Navigate to LinkedIn home feed and scroll naturally like a real user would during a casual browsing session.

========================================
STEP 1: NAVIGATION
========================================
- Go to https://www.linkedin.com/feed/
- Wait 2-3 seconds for page to fully load
- Verify you're on the feed page (look for posts, "Start a post" box, etc.)
- If login required, you should already be authenticated via saved session

========================================
STEP 2: HUMAN-LIKE SCROLLING BEHAVIOR
========================================
Scroll Pattern:
- Scroll down 300-600 pixels each time (variable distances)
- After each scroll, pause 2-5 seconds (randomize the pause duration)
- Occasionally scroll up 100-200 pixels (as if re-reading something interesting)
- Vary scrolling speed: sometimes slow, sometimes slightly faster
- Every 3-4 scrolls, pause longer (6-10 seconds) to simulate reading a post thoroughly

Engagement Simulation (Optional):
- Occasionally hover over a post (move mouse over it)
- Pause on posts with images or videos slightly longer
- Simulate natural reading patterns: start-stop-scroll-pause

Realistic Behaviors:
- Don't scroll in perfect intervals
- Don't maintain constant speed
- Mix scroll distances: small scrolls, medium scrolls
- Include micro-pauses (0.5-1 second) between some actions
- If you see a sponsored post, scroll past it faster
- If you see engaging content (images, polls, articles), pause longer

========================================
STEP 3: CONTENT OBSERVATION
========================================
While scrolling, take note of:
- Post types you encounter (text, image, video, article, poll, job posting, etc.)
- Authors/companies posting (don't list all, just observe diversity)
- Engagement levels (likes, comments visible)
- Sponsored vs organic content
- Any notable trends or topics appearing multiple times

========================================
LIMITS & SAFEGUARDS
========================================
Maximum Actions:
- Total session duration: 2-4 minutes maximum
- Don't scroll more than 15 times regardless of content

Stop Conditions (stop immediately if any occur):
1. You've reached the scroll limit
2. No new posts load after 3 consecutive scrolls (feed end detected)
3. LinkedIn shows "You're all caught up" message
4. You encounter an error or unexpected page state
5. Total time exceeds 3 minutes

========================================
STEP 4: OUTPUT SUMMARY
========================================
After completing the scroll session, provide:

FEED OVERVIEW:
- Total scrolls performed: [number]
- Approximate posts viewed: [estimate]
- Session duration: [time]

CONTENT BREAKDOWN:
- Most common post types: [list 2-3 types]
- Notable topics/themes: [1-2 sentences]
- Sponsored content frequency: [low/medium/high]

SAMPLE POSTS OBSERVED:
Mention 2-3 interesting posts you noticed (without personal details):
Example: "Post about AI trends in tech, video about remote work tips, article about market analysis"


========================================
IMPORTANT REMINDERS
========================================
✓ Mimic real human browsing - no robotic patterns
✓ Variable timing is key to avoiding detection
✓ Take your time - humans don't rush through feeds
✓ If LinkedIn shows any security checks (CAPTCHA, verification), STOP and report immediately
✓ Don't interact with posts (no likes, comments, clicks on profiles) - just scroll and observe
✓ Stay on the main feed - don't navigate to other LinkedIn sections

========================================
ERROR HANDLING
========================================
If you encounter:
- Login page: Report that authentication failed
- Network error: Report connectivity issue
- Unexpected page: Describe what you see and stop
- CAPTCHA/verification: STOP immediately and notify
""",


"FEED_SCROLL_WITH_LIKECOMMENT_COUNT": """
You are a browser automation agent. Browse the LinkedIn feed like a real human and collect data from up to 5 posts.

========================================
TRACK THESE COUNTERS
========================================
[POST_COUNT]   = 0   (posts collected)

Stop IMMEDIATELY when POST_COUNT reaches 5.

========================================
STEP 1 — GO TO FEED
========================================
Navigate to: https://www.linkedin.com/feed/
Wait 2–3 seconds for the page to load.

========================================
STEP 2 — SCROLL LIKE A HUMAN
========================================
- Scroll down 300–500px each time (vary the distance)
- Wait 2–4 seconds after each scroll (randomize)
- Every 3rd or 4th scroll, pause 5–8 seconds (simulating deep reading)
- Occasionally scroll UP 100–150px then back down (re-reading behavior)
- Scroll faster past sponsored posts
- Scroll slower near posts with images or long text

========================================
STEP 3 — COLLECT EACH POST
========================================
For every post on the feed:

1. Post content — read post content and collect post content .
  

2. Likes — reaction count shown below the post on left side (e.g. "👍 1,204").
   - Convert shorthand: 1.2K = 1200, 3.5M = 3500000
   - If shown as "X+", record the number before the "+"
   - If none visible, record 0

3. Comments — "X comments" shown below the post.
    Its on right side
   - If shown as "X+", record the number before the "+"
   - If none visible, record 0


Collect ONE post per action step. Do not batch multiple posts in a single step.

After recording each post:
→ Add 1 to [POST_COUNT]. If [POST_COUNT] >= 5 → STOP, go to output.

========================================
STEP 4 — OUTPUT
========================================
Print each post in this format:

POST 1
Likes: 1204
Comments: 64
Content: Post content 

POST 2
Likes: 342
Comments: 28
Content: Post content 

... continue for all posts ...


========================================
STOP CONDITIONS
========================================
Stop immediately if any of these occur:
- [POST_COUNT] hits 5
- CAPTCHA or security check appears → report it and stop
- Login page appears → report it and stop
- "You're all caught up" message appears → report it and stop
- Browser session shows any error → report it and stop
""",



"COPY_FEEDPOST_LINK": """
You are a browser automation agent. Collect post links from the LinkedIn feed
using the ••• menu on each post.

========================================
STEP 1 — NAVIGATE
========================================
Go to: https://www.linkedin.com/feed/
Wait 3 seconds. Session already active — do NOT log in.
If login page appears → report "Session expired" and stop.

========================================
STEP 2 — GET LINK FROM POST
========================================
Do this exact sequence for the first visible post:

  ── A. READ AUTHOR ──────────────────────────────
  Read the author name visible at the top of the post card.
  Store it. If not readable → use "Unknown".

  ── B. CLICK ••• BUTTON ─────────────────────────
  Find the button with aria-label containing "Open control menu"
  on this specific post card.
  Click it ONCE.
  Wait 2 seconds for the dropdown to fully open.
  If dropdown does not open after 2 seconds → skip this post.

  ── C. CLICK "Embed this post" ──────────────────
  In the open dropdown, find the item with visible text "Embed this post".
  Click it ONCE.
  Wait 2 seconds for the embed dialog to open.

 ── D. EXTRACT URN FROM INPUT ───────────────────
  After the embed dialog opens,:
in this section you will see a code in this format-
      <iframe src="https://www.linkedin.com/embed/feed/update/urn:li:share:7428286848096980992?collapsed=1"...
  copy this
      
  ── E. PARSE URN AND BUILD URL ──────────────────
from the copied value, find the part matching:
      urn:li:share:XXXXXXXXXXXXXXXXX

  Then build the final URL:
      https://www.linkedin.com/feed/update/urn:li:share:XXXXXXXXXXXXXXXXX

  Store as [POST_URL].

  ── F. CLOSE DIALOG ─────────────────────────────
  Press Escape key to close the embed dialog.
  Wait 1 second.

  ── G. RECORD ───────────────────────────────────
  Record:
    Author: [name]
    Link:   [POST_URL]

STRICT RULES:
- Click ONLY by aria-label or visible text — NEVER by index number
- NEVER click Like, Comment, Share, Follow, or Connect
- NEVER open a second ••• menu while another is still open
- Always close the embed dialog before moving to the next post
- If ••• click fails → skip this post

========================================
STEP 3 — OUTPUT
========================================
POST 1
Author: [name]
Link: https://www.linkedin.com/feed/update/urn:li:share:...

========================================
STOP CONDITIONS
========================================
- Login page → report and stop
- CAPTCHA → report and stop
- Embed dialog does not open → skip post and report
""",

 

"GET_FIRST_COMMENTER_FROM_FIFTH_POST": """
You are a browser automation agent.
Goal: Get the FIFTH post's FIRST commenter name and profile URL.

========================================
STEP 1 — NAVIGATE
========================================
Go to: https://www.linkedin.com/feed/
Wait 4 seconds.
Do NOT log in — session is already active.
If login page appears → stop and report "Session expired".

========================================
STEP 2 — OPEN FIFTH POST COMMENTS
========================================
Find the FIFTH real post on the feed.
Skip ads, promoted posts, "People you may know" widgets.

Find the comment COUNT text on that post:
  "48 comments" or "3 comments" or "1 comment"
It appears ABOVE the action buttons row.

⚠️ Do NOT click the "Comment" action button. That is for WRITING comments.
   You want the COUNT text ABOVE those buttons.

Click the comment COUNT text ONCE. Wait 3 seconds.

If no comment count exists → report "FIFTH post has no comments" and stop.

========================================
STEP 3 — GET FIRST COMMENTER
========================================
Once comments are loaded, :
look for the first comment with commentor name
find the <a> anchor tag that
 wraps the commenter's name.
 Read the href attribute of that <a> tag directly.
 → It will look like: https://www.linkedin.com/in/[username]/
  Extract:
    - Commenter name  (visible text inside the <a> tag)
  - Profile URL     (href attribute of the <a> tag)

Do NOT click anything. Do NOT open any new tab.
Read name and URL directly from the result.

If href does not contain "/in/" → store "URL not captured".

========================================
STEP 4 — OUTPUT
========================================
NAME:         [text from anchor tag]
PROFILE URL:  [href from anchor tag]

========================================
STOP CONDITIONS
========================================
- Login page → stop, report "Session expired"
- CAPTCHA → stop, report "CAPTCHA detected"
- No comments → stop, report it
- find_elements returns empty → output "URL not captured"
""",


"GET_COMMENTOR_URLS": """
You are a browser automation agent.

GOAL: Go to the LinkedIn feed, open the first real post's comments,
extract each commenter's profile URL directly from the anchor tag
wrapping their name in the comments section.

========================================
STEP 1 — NAVIGATE
========================================
Go to: https://www.linkedin.com/feed/
Wait 3 seconds.

========================================
STEP 2 — FOR FIRST POST
========================================
Record:
  - Post author name
  - First 20 words of post content

  ========================================
STEP 3 — OPEN COMMENTS
========================================
⚠️ IMPORTANT: Do NOT click the "Comment" button (which opens a text
input box to write a new comment). That is the WRONG button.

Instead, look for a clickable text that shows the comment COUNT, such as:
  - "12 comments"
  - "View 5 comments"
  - "1 comment"

This text is usually located ABOVE the Like/Comment/Share action bar,
just below the post's reaction count.

Click that comment COUNT link ONCE.
Wait 3 seconds for the existing comments to load.

If no comment count link is visible or count is 0 → report "No comments" and STOP

========================================
========================================
STEP 4 — EXTRACT COMMENTER NAMES + URLS FROM ANCHOR TAGS
========================================
You must scroll through the comments section and visit EACH comment
one by one. Do NOT try to read all comments at once.

Follow this sequence for EACH comment:

  4a. Scroll down SLOWLY until the next comment is fully visible
      on screen.
  4b. Focus on that single comment block.
  4c. Inside that comment block, find the <a> anchor tag that
      wraps the commenter's name.
  4d. Read the href attribute of that <a> tag directly.
      → It will look like: https://www.linkedin.com/in/[username]/
  4e. Extract:
        - Commenter name  (visible text inside the <a> tag)
        - Profile URL     (href attribute of the <a> tag)
  4f. Add this name + URL pair to your running list.
  4g. Scroll down to the NEXT comment and repeat from 4a.

⚠️ RULES:
  - Process ONE comment at a time, in order, top to bottom.
  - Do NOT skip any comment.
  - Do NOT click any profile link or open any new tab.
  - Do NOT navigate away from the post page.
  - Read the href directly from the DOM — no clicking needed.

If "Load more comments" button becomes visible at any point:
  → Click it. Wait 2 seconds.
  → Continue scrolling and processing new comments from 4a.
  → Repeat clicking "Load more" up to 3 times maximum.

Keep a running count as you go:
  Comment #1 → Name: [x] | URL: [y]
  Comment #2 → Name: [x] | URL: [y]
  ...and so on until no more comments remain.
========================================
STEP 5 — OUTPUT
========================================

⚠️ You MUST return ONLY a valid JSON object. No extra text, no markdown,
no explanation — just the raw JSON object below.

{
  "status": "success",
  "post": {
    "author": "[post author name]",
    "content_preview": "[first 20 words only]"
  },
  "commenters": [
    { "name": "[commenter name]", "url": "https://www.linkedin.com/in/[username]/" },
    { "name": "[commenter name]", "url": "https://www.linkedin.com/in/[username]/" }
  ],
  "summary": {
    "total_extracted": [number],
    "failed": [number]
  }
}

========================================
STOP CONDITIONS
========================================
- No comments → report "No comments" and stop
- CAPTCHA → output what you have and stop
- Login page → output what you have and stop
- Any browser crash → output what you have and stop
""",



"CHECK_CONNECTION": """
You are an intelligent browser automation agent.

GOAL:
CHECK IF THE PERSON IS CONNECTION OR NOT

----------------------------------------
LOGIN
----------------------------------------
1. Open https://www.linkedin.com/login
2. Log in using provided sensitive credentials.
3. Wait for homepage to load.

----------------------------------------
SEARCH STRATEGY
----------------------------------------
1. Locate the global search bar at the top of the LinkedIn page.
2. Click the search bar.
3. Type EXACTLY : Hitesh Choudhary
4. Press Enter to execute the search.
5. Wait for search results to load completely.
6. From the People results section, identify the profile that matches:
   - Name: Hitesh Choudhary
   - Profession: YouTuber (or similar creator/educator description)
7. Click the correct profile result.
8. Wait until the profile page fully loads.

=======================================
TASK: CHECK CONNECTION STATUS
=======================================

GOAL:
Determine the relationship status between me and the currently opened LinkedIn profile.

STRICT RULES:
- Only interact with elements in the top profile header section.
- Do NOT scroll.
- Do NOT open new tabs.
- Do NOT click "Message" or "Follow".
- Only click the three-dot (More) menu next to the Message/Follow buttons.
- Perform exactly one click action.
- After reading the modal, do not click anything else.

STEPS:

1. Locate the three-dot (More) button in the profile header.
2. Click the three-dot button.
3. Wait for the dropdown/modal menu to fully render.
4. Inspect the visible options in the opened menu.

DECISION LOGIC:

If the menu contains:
- "Remove Connection" → RETURN: "ALREADY_CONNECTED"
- "Connect" → RETURN: "NOT_CONNECTED"
- "Pending" → RETURN: "REQUEST_PENDING"

If none of these options are present → RETURN: "UNKNOWN"

OUTPUT FORMAT (STRICT JSON ONLY):

{
  "connection_status": "ALREADY_CONNECTED | NOT_CONNECTED | REQUEST_PENDING | UNKNOWN",
  "evidence": "Exact text found inside the modal"
}

Do not guess.
Do not assume.
Base the decision only on visible menu text.

----------------------------------------

----------------------------------------

""",



"VIEW_ACTIVITY_POST": """
You are an intelligent browser automation agent.

GOAL:
Find the LinkedIn profile of "Utkarsh Deoli" who works at "Crux Sphere Technology",
navigate to their Activity section, click on Posts,
and extract the content of up to 5 posts (or fewer if less exist).

========================================
COUNTERS & TRACKERS
========================================
[POST_COUNT]       = 0
[POSTS_COLLECTED]  = []
[MAX_POSTS]        = 5

========================================
PHASE 1 — NAVIGATE TO LINKEDIN
========================================

STEP 1 — GO TO LINKEDIN FEED
Navigate to: https://www.linkedin.com/feed/
Wait 3 seconds. Session already active — do NOT log in.
If login page appears → report "Session expired" and stop.

========================================
PHASE 2 — SEARCH FOR THE PERSON
========================================

STEP 2 — USE LINKEDIN SEARCH BAR
Click on the LinkedIn search bar at the top of the page.
Type exactly: Utkarsh Deoli Crux Sphere Technology
Wait 2 seconds.
Press Enter OR click the search icon.
Wait 3 seconds for results to load.

----------------------------------------
STEP 3 — FILTER BY PEOPLE
----------------------------------------
After results load, look for filter tabs near the top of the results page.
Find the tab labeled "People" and click it ONCE.
Wait 3 seconds for filtered results to load.

If "People" tab is not visible:
→ Look for "See all results" and click it first
→ Then click the "People" tab
→ Wait 3 seconds

========================================
PHASE 3 — IDENTIFY THE CORRECT PROFILE
========================================

STEP 4 — SCAN RESULTS FOR CORRECT PERSON
Look through the visible people results ONE AT A TIME.

For each result card:
  → Read the person's display name
  → Read the subtitle/tagline (usually shows job title and company)

  Check if BOTH conditions are true:
    ✓ Name contains "Utkarsh Deoli" (exact or close match)
    ✓ Subtitle/tagline mentions "Crux Sphere Technology"

  IF BOTH match → this is the target profile. Proceed to STEP 5.
  IF name matches but company does NOT → skip this result.
  IF neither matches → move to next result card.

If no match found on first page:
→ Scroll down 300px, wait 2 seconds, check newly visible results
→ Repeat up to 3 scrolls maximum
→ If still no match found after 3 scrolls →
   report "Profile not found for Utkarsh Deoli at Crux Sphere Technology" and stop.

========================================
PHASE 4 — OPEN PROFILE
========================================

STEP 5 — CLICK ON TARGET PROFILE
Click on the name "Utkarsh Deoli" in the matched result card.
Wait 4 seconds for the profile page to fully load.


If any check fails → press Back, return to results, try the next matching card.

Store current URL using execute_script:
    return window.location.href;
Store as [PROFILE_URL].

========================================
PHASE 5 — NAVIGATE TO ACTIVITY SECTION
========================================

STEP 6 — FIND AND CLICK "ACTIVITY" SECTION
Scroll down slowly from the top of the profile page.
Look for a section labeled "Activity".

  ── A. CLICK "Show all " ────────────────
  Inside the Activity section, find a button or link
  with text like:
    - "Show all"
    
  Click it ONCE.
  Wait 3 seconds for the Activity page to load.

  ── C. CONFIRM ACTIVITY PAGE LOADED ─────────────
  Check that:
    ✓ Page URL contains "recent-activity"
    ✓ Content is visible (posts/activity items)

  If page fails to load → report "Activity page failed to load" and stop.

========================================
PHASE 6 — CLICK "POSTS" FILTER
========================================

STEP 7 — SWITCH TO POSTS TAB
On the Activity page, look for filter tabs near the top.
These may include: "All", "Posts", "Comments", "Reactions", "Articles"

Find the tab labeled "Posts" and click it ONCE.
Wait 3 seconds for the Posts feed to load.

If "Posts" tab is NOT visible:
→ Scroll up to the top of the activity page
→ Look again for filter/tab row
→ If still not found → report "Posts tab not found" and stop.

Confirm Posts tab is now active:
  ✓ "Posts" tab appears selected/highlighted
  ✓ Feed below shows post content authored by Utkarsh Deoli

========================================
PHASE 7 — COLLECT POST CONTENT
========================================

STEP 8 — READ POST CONTENT ONE BY ONE
Collect up to [MAX_POSTS] = 5 posts.
Process each visible post card ONE AT A TIME, top to bottom.

For each post:

  ── A. READ POST TEXT ───────────────────────────
  Read all visible text content inside the post card.
  This includes the main body text of the post.

  If post text is truncated with "...see more" or "more":
  → Click "...see more" ONCE
  → Wait 2 seconds
  → Read the now-fully-expanded post text

  Store the full text as [POST_CONTENT].

  If no text is found (image-only or video-only post):
  → Store [POST_CONTENT] = "[Media only — no text content]"

  ── B. READ POST METADATA (optional) ────────────
  Also read if visible:
    [POST_DATE]   → Relative date/time shown on post (e.g. "3d", "1w")
    [POST_LIKES]  → Reaction/like count if shown
    [POST_TYPE]   → "Text", "Image", "Video", "Article", "Repost"

  ── C. RECORD AND COUNT ─────────────────────────
  Add to [POSTS_COLLECTED]:
    Post number:  [POST_COUNT + 1]
    Date:         [POST_DATE]
    Type:         [POST_TYPE]
    Likes:        [POST_LIKES]
    Content:      [POST_CONTENT]

  Add 1 to [POST_COUNT].
  If [POST_COUNT] >= 5 → STOP collecting. Go to STEP 9.

----------------------------------------
STEP 8B — SCROLL IF FEWER THAN 5 POSTS VISIBLE
----------------------------------------
If fewer than 5 posts are visible and [POST_COUNT] < 5:
→ Scroll down 400–500px
→ Wait 3 seconds for new posts to load
→ Continue collecting newly visible posts
→ Repeat scrolling up to 5 times maximum

If after 5 scrolls [POST_COUNT] is still less than 5:
→ Report: "Only [POST_COUNT] posts found. Returning all available."
→ Proceed to STEP 9 with whatever was collected.

If NO posts are found at all on the Posts tab:
→ Report: "No posts found on Utkarsh Deoli's profile."
→ Stop and output summary.

STRICT RULES (Phase 7):
- Read content only — do NOT click Like, Comment, Share, or React
- Do NOT follow or connect with the profile
- Click "...see more" ONLY to expand post text — nothing else
- If a post card is an ad or promoted content → skip it, do not count it
- Process posts in order: top = Post 1, next = Post 2, and so on

========================================
STEP 9 — FINAL OUTPUT
========================================

PROFILE DETAILS
───────────────
Full Name:   Utkarsh Deoli
Company:     Crux Sphere Technology
Profile URL: [PROFILE_URL]

────────────────────────────────────────
POST 1
────────────────────────────────────────
Date:     [POST_DATE]
Type:     [POST_TYPE]
Likes:    [POST_LIKES]
Content:
[POST_CONTENT]

────────────────────────────────────────
POST 2
────────────────────────────────────────
Date:     [POST_DATE]
Type:     [POST_TYPE]
Likes:    [POST_LIKES]
Content:
[POST_CONTENT]

────────────────────────────────────────
POST 3
────────────────────────────────────────
Date:     [POST_DATE]
Type:     [POST_TYPE]
Likes:    [POST_LIKES]
Content:
[POST_CONTENT]

────────────────────────────────────────
POST 4
────────────────────────────────────────
Date:     [POST_DATE]
Type:     [POST_TYPE]
Likes:    [POST_LIKES]
Content:
[POST_CONTENT]

────────────────────────────────────────
POST 5
────────────────────────────────────────
Date:     [POST_DATE]
Type:     [POST_TYPE]
Likes:    [POST_LIKES]
Content:
[POST_CONTENT]

---
SUMMARY
Profile found:       Yes / No
Activity page found: Yes / No
Posts tab found:     Yes / No
Total posts found:   X
Posts collected:     X out of 5
---

========================================
STOP CONDITIONS
========================================
- Login page appears                    → report "Session expired" and stop
- CAPTCHA encountered                   → report "CAPTCHA detected" and stop
- Profile not found after 3 scrolls     → report "Profile not found" and stop
- Activity page fails to load           → report "Activity page failed to load" and stop
- Posts tab not found                   → report "Posts tab not found" and stop
- No posts found at all                 → report "No posts available" and stop
- [POST_COUNT] >= 5                     → stop and output
- 5 scrolls with no new posts loading   → stop and output what was collected
""",


"VIEW_ACTIVITY_COMMENTS": """
You are an intelligent browser automation agent.

GOAL:
Find the LinkedIn profile of "Utkarsh Deoli" who works at "Crux Sphere Technology",
navigate to their Activity section, click on Comments tab,
collect comments across posts and return,


========================================
COUNTERS & TRACKERS
========================================
[COMMENT_COUNT]      = 0
[COMMENTS_COLLECTED] = []
[MAX_COMMENTS]       = 10
[SCROLL_COUNT]       = 0
[MAX_SCROLLS]        = 5

========================================
PHASE 1 — NAVIGATE TO LINKEDIN
========================================

STEP 1 — GO TO LINKEDIN FEED
Navigate to: https://www.linkedin.com/feed/
Wait 3 seconds. Session already active — do NOT log in.
If login page appears → report "Session expired" and stop.

========================================
PHASE 2 — SEARCH FOR THE PERSON
========================================

STEP 2 — USE LINKEDIN SEARCH BAR
Click on the LinkedIn search bar at the top of the page.
Type exactly: Utkarsh Deoli Crux Sphere Technology
Wait 2 seconds.
Press Enter OR click the search icon.
Wait 3 seconds for results to load.

========================================
PHASE 3 — IDENTIFY THE CORRECT PROFILE
========================================

STEP 3 — SCAN SEARCH RESULTS FOR CORRECT PERSON
You should now be on the search results page (unless you clicked 
autocomplete and went directly to profile).

Look through the visible people results ONE AT A TIME.

For each result card:
  → Read the person's display name
  → Read the subtitle/tagline (shows job title and company)

  Check if BOTH conditions are true:
    ✓ Name contains "Utkarsh Deoli" (exact or close match)
    ✓ Subtitle mentions "Crux Sphere Technology" or "Crux Sphere"

  IF BOTH match → this is the target profile. Proceed to STEP 4.
  IF name matches but company does NOT → skip this result.
  IF neither matches → move to next result card.

If no match found on first page:
→ Scroll down 300px, wait 2 seconds, check newly visible results
→ Repeat up to 3 scrolls maximum
→ If still no match → report "Profile not found" and stop.

========================================
PHASE 4 — OPEN PROFILE
========================================

STEP 4 — CLICK ON TARGET PROFILE (if not already on it)
If you clicked autocomplete in STEP 2C, you should already be on 
Utkarsh's profile. Check the URL - if it contains "/in/utkarsh" 
then skip the click and proceed to profile confirmation.

Otherwise:
Click on the name "Utkarsh Deoli" in the matched result card.
Wait 4 seconds for the profile page to fully load.

  ── CONFIRM CORRECT PROFILE ─────────────────
  Verify you are on the correct page:
    ✓ Page URL contains "/in/"
    ✓ Profile name displayed matches "Utkarsh Deoli"
    ✓ Current or past experience shows "Crux Sphere Technology"

  If any check fails:
    → Press browser Back button
    → Return to search results
    → Try the next matching result card

  ── STORE PROFILE URL ───────────────────────
  Execute JavaScript to get and store the profile URL:
      return window.location.href;
  
  Store as [PROFILE_URL].
  
  Example: [PROFILE_URL] = "https://www.linkedin.com/in/utkarshdeoli/"

========================================
PHASE 5 — NAVIGATE TO ACTIVITY SECTION
========================================

STEP 5 — ACCESS ACTIVITY VIA UI (PRIMARY METHOD)
On Utkarsh Deoli's profile page, scroll down to find the Activity section.

  ── A. LOCATE ACTIVITY SECTION ──────────────
  Scroll down slowly on the profile page.
  Look for a section labeled "Activity" or "Recent Activity".
 

  ── B. CLICK "SHOW ALL" OR "SEE ALL ACTIVITY" ───
  Inside the Activity section, look for a link/button that says:
    • "Show all"
  
  Click it ONCE.
  Wait 3 seconds for the full Activity page to load.

  ── C. NAVIGATE TO COMMENTS TAB ─────────────
  On the Activity page, look for filter tabs near the top:
    • "All"
    • "Posts"  
    • "Comments"
    • "Reactions"
    • "Articles"
  
  Find and click the "Comments" tab.
  Wait 3 seconds for the Comments feed to load.

  Confirm Comments tab is active:
    ✓ URL contains "recent-activity/comments"
    ✓ "Comments" tab appears selected/highlighted
    ✓ Feed shows comment cards

  ── D. FALLBACK: DIRECT URL NAVIGATION ──────
  If Activity section is NOT visible after scrolling:
    → Navigate directly to:
      [PROFILE_URL]recent-activity/comments/
    → Example: "https://www.linkedin.com/in/utkarshdeoli/recent-activity/comments/"
    → Wait 4 seconds for page to load

  If page fails to load even with URL method:
    → Report "Comments page failed to load" and stop.

========================================


========================================
PHASE 6 — MANUAL HUMAN-LIKE COMMENT COLLECTION
========================================

GOAL:
Simulate a real human manually browsing the Comments activity feed.
Open each comment naturally, read it, store it,
then scroll slowly to the next one.

Do NOT mass-extract all DOM elements at once.
Process ONE visible comment at a time.

----------------------------------------
INITIALIZE TRACKERS
----------------------------------------

[COMMENT_COUNT]      = 0
[COMMENTS_COLLECTED] = []
[SCROLL_COUNT]       = 0
[MAX_COMMENTS]       = 10
[MAX_SCROLLS]        = 10
[NO_NEW_COMMENT_RUN] = 0
[MAX_EMPTY_SCROLLS]  = 2

----------------------------------------
STEP 6.1 — HUMAN-LIKE VIEWING BEHAVIOR
----------------------------------------

1. Stay on the Comments tab page.
2. Do NOT inspect entire DOM.
3. Focus only on the top-most fully visible comment card.
4. Pretend you are a human reading it.

Pause 2–4 seconds before interacting.

----------------------------------------
STEP 6.2 — PROCESS ONE COMMENT AT A TIME
----------------------------------------

For the FIRST fully visible comment card:

  A. Scroll slightly so the card is centered on screen.
     Wait 2 seconds.

  B. If "See more" appears in:
       
        - Utkarsh's comment
     Click it once.
     Wait 2 seconds.

  C. Manually read and extract:

    
        [COMMENT_TEXT]
        → Capture full visible text of Utkarsh's comment.

        [COMMENT_DATE]
        → If visible.

        [COMMENT_LIKES]
        → If visible, else set to 0.

  D.      Append to [COMMENTS_COLLECTED]
            Increment [COMMENT_COUNT] += 1

  E. Natural pause:
        Wait 2–5 seconds before scrolling.

----------------------------------------
STEP 6.3 — NATURAL SCROLL BEHAVIOR
----------------------------------------

After processing current comment:

  Scroll down slowly 400–600 pixels.
  Do NOT jump to bottom.
  Wait 3–4 seconds for content to load.

  Increment:
      [SCROLL_COUNT] += 1

  If new comment card appears:
      Reset [NO_NEW_COMMENT_RUN] = 0
  Else:
      Increment [NO_NEW_COMMENT_RUN] += 1

----------------------------------------
ANTI-RATE-LIMIT RULES
----------------------------------------

• Never scroll more than once every 3 seconds.
• Never extract more than one comment per scroll.
• Do not query entire page repeatedly.
• Avoid rapid clicking.
• Act like a slow reader.

If LinkedIn shows:
  - Blank feed
  - Sudden redirect
  - Unusual loading behavior

Stop immediately and report:
  "Rate limit likely triggered"

----------------------------------------
STOP CONDITIONS
----------------------------------------

Stop when ANY of the following:

  ✓ [COMMENT_COUNT] >= [MAX_COMMENTS]
  ✓ [SCROLL_COUNT] >= [MAX_SCROLLS]
  ✓ [NO_NEW_COMMENT_RUN] >= [MAX_EMPTY_SCROLLS]
  ✓ Page shows "End of results"
  ✓ No new content loads after 2 slow scrolls

Then proceed to PHASE 7 for analysis.

----------------------------------------
DATA STRUCTURE FORMAT
----------------------------------------

Store each comment as:

{
  "date": "[COMMENT_DATE]",
  "likes": "[COMMENT_LIKES]",
  "comment_text": "[COMMENT_TEXT]"
}

========================================
END OF PHASE 6
========================================


========================================
STEP 9 — FINAL OUTPUT
========================================

Output the analysis in plain text format (NOT as a file to avoid encoding issues).
Use simple ASCII characters only.

PROFILE DETAILS
---------------
Full Name:   Utkarsh Deoli
Company:     Crux Sphere Technology
Profile URL: [PROFILE_URL]

========================================
COMMENTS COLLECTED
========================================

----------------------------------------
COMMENT 1
----------------------------------------
Date:               [COMMENT_DATE]
Likes:              [COMMENT_LIKES]
Original post about:[ORIGINAL_POST_CONTEXT]
His comment:        [COMMENT_TEXT]


----------------------------------------
COMMENT 2
----------------------------------------
Date:               [COMMENT_DATE]
Likes:              [COMMENT_LIKES]
Original post about:[ORIGINAL_POST_CONTEXT]
His comment:        [COMMENT_TEXT]


========================================



========================================
SUMMARY
========================================
Profile found:         Yes / No
Comments page found:   Yes / No
Total comments found:  [COMMENT_COUNT]
Comments collected:    [COMMENT_COUNT] out of 10
Scrolls performed:     [SCROLL_COUNT]

========================================

IMPORTANT NOTES:
- Do NOT create files - output analysis as plain text
- Use only ASCII characters in output (no fancy Unicode)
- Extract tool returns data automatically - just process it
- Scroll between extractions to load new comments

========================================
STOP CONDITIONS
========================================
- Login page appears                     → "Session expired" and stop
- CAPTCHA encountered                    → "CAPTCHA detected" and stop
- Profile not found after 3 scrolls      → "Profile not found" and stop
- Comments page fails to load            → "Comments page failed to load" and stop
- No new comments after 2 scrolls        → stop collecting, do analysis

========================================
ERROR RECOVERY
========================================
If browser crashes:
  1. Navigate to: https://www.linkedin.com/feed/
  2. Wait 3 seconds
  3. Resume from PHASE 2

If stuck in loop (same action fails 3+ times):
  1. Switch to direct URL navigation
  2. Skip to next phase
""",





"GET_PROFILE_BIO": """
You are an intelligent browser automation agent.

GOAL:
Find the LinkedIn profile of "Utkarsh Deoli" who works at "Crux Sphere Technology"
and extract their full profile bio / About section.

========================================
PHASE 1 — NAVIGATE TO LINKEDIN
========================================

STEP 1 — GO TO LINKEDIN FEED
Navigate to: https://www.linkedin.com/feed/
Wait 3 seconds. Session already active — do NOT log in.
If login page appears → report "Session expired" and stop.

========================================
PHASE 2 — SEARCH FOR THE PERSON
========================================

STEP 2 — USE LINKEDIN SEARCH BAR
Click on the LinkedIn search bar at the top of the page.
Type exactly: Utkarsh Deoli Crux Sphere Technology
Wait 2 seconds.
Press Enter OR click the search icon.
Wait 3 seconds for results to load.

----------------------------------------
STEP 3 — FILTER BY PEOPLE
----------------------------------------
After results load, look for filter tabs near the top of the results page.
Find the tab labeled "People" and click it ONCE.
Wait 3 seconds for filtered results to load.

If "People" tab is not visible:
→ Look for "See all results" and click it first
→ Then click the "People" tab
→ Wait 3 seconds

========================================
PHASE 3 — IDENTIFY THE CORRECT PROFILE
========================================

STEP 4 — SCAN RESULTS FOR CORRECT PERSON
Look through the visible people results ONE AT A TIME.

For each result card:
  → Read the person's display name
  → Read the subtitle/tagline (usually shows job title and company)

  Check if BOTH conditions are true:
    ✓ Name contains "Utkarsh Deoli" (exact or close match)
    ✓ Subtitle/tagline mentions "Crux Sphere Technology"

  IF BOTH match → this is the target profile. Proceed to STEP 5.
  IF name matches but company does NOT → skip this result.
  IF neither matches → move to next result card.

If no match found on first page:
→ Scroll down 300px, wait 2 seconds, check newly visible results
→ Repeat up to 3 scrolls maximum
→ If still no match found after 3 scrolls →
   report "Profile not found for Utkarsh Deoli at Crux Sphere Technology" and stop.

========================================
PHASE 4 — OPEN PROFILE
========================================

STEP 5 — CLICK ON TARGET PROFILE
Click on the name "Utkarsh Deoli" in the matched result card.
Wait 4 seconds for the profile page to fully load.

Confirm you are on the correct page by checking:
  ✓ Page URL contains "/in/"
  ✓ Profile name displayed matches "Utkarsh Deoli"
  ✓ Current company or experience shows "Crux Sphere Technology"

If any check fails → press Back, return to results, try the next matching card.

========================================
PHASE 5 — EXTRACT PROFILE BIO
========================================

STEP 6 — LOCATE THE ABOUT / BIO SECTION
Scroll down slowly from the top of the profile page.
Look for a section labeled "About".

  ── A. IF "About" SECTION IS VISIBLE ────────────
  Read ALL text content inside the About section fully.
  This is the profile bio.

  If the bio is truncated with a "...see more" link:
  → Click "...see more" ONCE
  → Wait 2 seconds
  → Read the now-fully-expanded bio text

  Store the complete text as [PROFILE_BIO].

  ── B. IF NO "About" SECTION EXISTS ─────────────
  Report: "No About/Bio section found on this profile."
  Set [PROFILE_BIO] = "Not available"

STEP 7 — EXTRACT SUPPORTING DETAILS
While on the profile page, also collect:

  [FULL_NAME]      → Name shown at top of profile
  [HEADLINE]       → Tagline/headline text shown below name
  [LOCATION]       → Location shown on profile (if visible)
  [COMPANY]        → Current company from Experience section
                     (confirm it shows "Crux Sphere Technology")
  [PROFILE_URL]    → Current page URL from browser address bar
                     using execute_script:
                         return window.location.href;

STRICT RULES:
- Do NOT click Follow, Connect, Message, or any action button
- Do NOT like, comment on, or interact with any posts on the profile
- Read only — no writing, no form submissions
- If profile is private/restricted → report "Profile is private" and stop

========================================
STEP 8 — FINAL OUTPUT
========================================

PROFILE FOUND
─────────────
Full Name:   [FULL_NAME]
Headline:    [HEADLINE]
Location:    [LOCATION]
Company:     [COMPANY]
Profile URL: [PROFILE_URL]

PROFILE BIO (About Section)
────────────────────────────
[PROFILE_BIO]

---
SUMMARY
Profile found:        Yes / No
About section found:  Yes / No
Bio length (chars):   X
---

========================================
STOP CONDITIONS
========================================
- Login page appears              → report "Session expired" and stop
- CAPTCHA encountered             → report "CAPTCHA detected" and stop
- Profile not found after 3 scrolls → report "Profile not found" and stop
- Profile is private/restricted   → report "Profile is private" and stop
- Page fails to load after 3 attempts → report "Page load failed" and stop
""",


    "SEARCH_JOB": """
You are an intelligent browser automation agent.

GOAL:
Search LinkedIn Jobs for "MERN Stack" roles and retrieve details of the 10th job post.

----------------------------------------
LOGIN
----------------------------------------
1. Open https://www.linkedin.com/feed
3. Wait for homepage to load.

----------------------------------------
SEARCH STRATEGY
----------------------------------------
1. Navigate to the search bar.
2. Type "MERN Stack" and press enter.
3. click on Jobs filter from the filter bar .
4 wait for 3 sec for page to load
5. click on 'EASY APPLY' filter.
6. Wait for 3 sec for filtered results to load.

----------------------------------------
NAVIGATION RULES
----------------------------------------
- Scroll gradually through job listings.
- Stop when the 10th job card becomes visible.
- Open the 10th job posting.
- Extract full job description and company details.

----------------------------------------
LIMITS
----------------------------------------
- Maximum scroll actions: 15
- If results fail to load after 3 attempts, terminate.

----------------------------------------
OUTPUT FORMAT
----------------------------------------
Return:

{
  "job_title": "",
  "company": "",
  "location": "",
  "job_description": ""
}
""",


  "EXTRACT_BIO": """
You are a browser automation agent.

GOAL: Find Utkarsh Deoli on LinkedIn and extract their bio/About section.

========================================
STEP 1 — NAVIGATE TO FEED
========================================
Go to: https://www.linkedin.com/feed/
Wait 3 seconds.

========================================
STEP 2 — SEARCH
========================================

Click the search bar at the top.
Type: Utkarsh Deoli Crux Sphere Technology
Press Enter. Wait 3 seconds.

Click "People" from filter tab. Wait 3 seconds.

========================================
STEP 3 — FIND CORRECT PROFILE
========================================
For each result card check:
  ✓ Name matches "Utkarsh Deoli"
  ✓ Tagline mentions "Crux Sphere Technology"

If both match → proceed to STEP 4.
If no match → scroll 300px, wait 2 seconds, repeat.
After 3 scrolls with no match → report "Profile not found" and STOP.

========================================
STEP 4 — OPEN PROFILE
========================================
Click the matched profile name. Wait 4 seconds.
Verify:
  ✓ URL contains "/in/"
  ✓ Name shows "Utkarsh Deoli"
If wrong page → go back and try next result.

========================================
STEP 5 — EXTRACT BIO
========================================
The bio is visible at the top of the profile, just below the person's profile image and name . It is a short paragraph describing who they are.

Read and record ALL visible bio text.
Do NOT click anything to expand — only read what is already visible.
If no bio is present, record "Not available".

========================================
STEP 6 — OUTPUT
========================================
Return exactly this JSON:

{
  "name": "Utkarsh Deoli",
  "bio": "[full bio text or 'Not available']"
}

========================================
STOP CONDITIONS
========================================
- Profile not found → bio: "Profile not found"
- CAPTCHA → bio: "failed: CAPTCHA detected"
- Login page → bio: "failed: Session expired"
""",


"EXTRACT_EDUCATION_EXPERIENCE": """
You are a browser automation agent.

GOAL: Find Utkarsh Deoli on LinkedIn and extract their Education and Experience.

========================================
STEP 1 — NAVIGATE TO FEED
========================================
Go to: https://www.linkedin.com/feed/
Wait 3 seconds.

========================================
STEP 2 — SEARCH
========================================
Click the search bar at the top.
Type: Utkarsh Deoli Crux Sphere Technology
Press Enter. Wait 3 seconds.

Click "People" from filter tab. Wait 3 seconds.

========================================
STEP 3 — FIND CORRECT PROFILE
========================================
For each result card check:
  ✓ Name matches "Utkarsh Deoli"
  ✓ Tagline mentions "Crux Sphere Technology"

If both match → proceed to STEP 4.
If no match → scroll 300px, wait 2 seconds, repeat.
After 3 scrolls with no match → report "Profile not found" and STOP.

========================================
STEP 4 — OPEN PROFILE
========================================
Click the matched profile name. Wait 2 seconds.

========================================

   STEP 6 — EXTRACT EXPERIENCE
========================================
Scroll down until "Experience" section heading is visible.

IMPORTANT — Check for "Show all" button:
- Look for a button or link that says  "Show all" 
  directly below the Experience section entries.
- If visible → click it. Wait 3 seconds. Then use read_long_content to
  read all expanded experience entries.
  and then go back to previous page
- If not visible → read the entries already shown.

For each experience entry record:
  - Job title
  - Company name
  - Duration (start date – end date or "Present")

If no Experience section found → record "Not available".

========================================
STEP 7 — EXTRACT EDUCATION
========================================
Continue scrolling down until "Education" section heading is visible.

IMPORTANT — Check for "Show all" button:
- Look for a button or link that says "Show all X educations" or "Show all"
  directly below the Education section entries.
- If visible → click it. Wait 3 seconds. Then use read_long_content to
  read all expanded education entries.
  and then go back to previous page
- If not visible → read the entries already shown.

For each education entry record:
  - School/University name
  - Degree and field of study
  - Years attended

If no Education section found → record "Not available".

⚠️ CRITICAL: Always check for and click "Show all" before finalizing
education or experience data. Missing this step means incomplete data.




========================================
STEP 7 — OUTPUT
========================================
Return exactly this JSON:

{
  "name": "Utkarsh Deoli",
  "experience": [
    {
      "title": "",
      "company": "",
      "duration": ""
    }
  ],
  "education": [
    {
      "school": "",
      "degree": "",
      "years": ""
    }
  ]
}

========================================
STOP CONDITIONS
========================================
- Profile not found → return all fields as "Profile not found"
- CAPTCHA → return all fields as "failed: CAPTCHA detected"
- Login page → return all fields as "failed: Session expired"
""",


"SEND_CONNECTION_REQ": """
You are a browser automation agent.

GOAL: Find Utkarsh Deoli on LinkedIn and send a connection request with a note.

========================================
STEP 1 — NAVIGATE TO FEED
========================================
Go to: https://www.linkedin.com/feed/
Wait 3 seconds.

========================================
STEP 2 — SEARCH
========================================
Click the search bar at the top.
Type: Utkarsh Deoli Crux Sphere Technology
Press Enter. Wait 2 seconds.

Click "People" from filter tab. Wait 2 seconds.

========================================
STEP 3 — FIND CORRECT PROFILE
========================================
For each result card check:
  ✓ Name matches "Utkarsh Deoli"
  ✓ Tagline mentions "Crux Sphere Technology"

If both match → proceed to STEP 4.
If no match → scroll 300px, wait 2 seconds, repeat.
After 3 scrolls with no match → report "Profile not found" and STOP.

========================================
STEP 4 — OPEN PROFILE
========================================
Click the matched profile name. Wait 2 seconds.



   ========================================
STEP 5 — CHECK CONNECTION STATUS
========================================
Click the "..." (More) button next to Message/Follow button.
Wait 2 seconds for dropdown to fully appear.
Read ALL options in the dropdown carefully.

- If dropdown contains "Remove Connection":
  → Press Escape. STOP. Return "already_connected".

- If dropdown contains "Withdraw":
  → Press Escape. STOP. Return "request_pending".

- If dropdown contains "Connect":
  → This means NOT connected. Click "Connect" from the dropdown.
  → Wait 2 seconds.
  → A dialog box will appear on screen. This is the CONNECTION REQUEST DIALOG.
  → Do NOT stop here. Do NOT report pending. Continue to STEP 6.

========================================
STEP 6 — COMPLETE THE CONNECTION DIALOG
========================================
After clicking Connect, a dialog appears with these options:
  - "Send without a note"  
  - "Add a note"

This dialog means the request has NOT been sent yet.
You MUST complete it.

→ Click "Add a note" button. Wait 1 second.
→ A text box appears. Click inside it.
→ Type exactly:
   Testing browser use AI agent and it works
→ Click the "Send" button.
→ Wait 2 seconds.

Only after clicking Send is the request actually sent.
Return connection_status: "sent"

STOP IMMEDIATELY after Send. Do not click anything else.

   


========================================
STEP 7 — OUTPUT
========================================
Return exactly this JSON:

{
  "name": "Utkarsh Deoli",
  "connection_status": "sent "
}

========================================
STOP CONDITIONS
========================================
- Max 1 request — never send more than once
- Profile not found → connection_status: "failed"
- CAPTCHA → connection_status: "failed: CAPTCHA detected"  
- Login page → connection_status: "failed: Session expired"
- Any error → output what you have and STOP
""",


"LINKEDIN_JOB_APPLY_ANALYSIS": """
OBJECTIVE: Find and analyze full stack developer jobs on LinkedIn that match my MERN stack expertise.

STEP 1 - SEARCH SETUP:
Navigate to LinkedIn Jobs (https://www.linkedin.com/jobs/)

In the search box at the top of page:
  - Enter keyword: "full stack developer" and press enter


  - Click on jobs tag

  wait for 3 sec for page to load 

  - Click on "Easy Apply" filter from filter bar
   - Click on "Under 10 applicants"filter from filter bar
  - Click on "Date Posted dropdown" filter from filter bar a dropdown appeans select Past 24 hours''
  - Apply filters and wait for results to load

STEP 2 - BROWSE JOBS (Human-like behavior):
Go through up to 20 job listings with realistic behavior:
  - Scroll down the job list slowly (simulate reading)
  - Pause 2-4 seconds between each scroll
  - Click on each job listing to view full description
  - Spend 5-10 seconds reading each job description
  - Occasionally scroll within the job description
  - Move back to job list and continue
  - Vary your timing - don't be robotic

STEP 3 - DATA COLLECTION:
For each job, extract and note:
  - Job Title
  - Company Name
  - Location/Remote status
  - Required Technologies (look for: MongoDB, Express, React, Node.js, JavaScript, TypeScript, etc.)
  - Required Experience (years)
  - Job Type (Full-time, Contract, etc.)
  - Salary Range (if mentioned)
  - Key Responsibilities
  - Required vs Preferred Skills
  - Company size/type if visible

STEP 4 - ANALYSIS:
MY PROFILE FOR COMPARISON:
  - Role: Full Stack Web Developer
  - Core Stack: MongoDB, Express.js, React.js, Node.js (MERN)
  - Specialization: JavaScript ecosystem

For each job, calculate:

1. TECH STACK MATCH (0-100%):
   - +25% for each MERN technology explicitly mentioned (MongoDB, Express, React, Node)
   - Bonus points if JavaScript/TypeScript emphasized
   - Deduct points if non-JS stacks are primary requirements (Java, Python backend, etc.)

2. EXPERIENCE MATCH:
   - Note if I meet the years required
   - Flag if unrealistic (e.g., "5+ years React experience" when React is only 10 years old)

3. ROLE ALIGNMENT:
   - Is it truly full stack or heavily skewed frontend/backend?
   - Are there deal-breakers? (heavy DevOps, mobile dev, etc.)

4. OPPORTUNITY QUALITY:
   - Company reputation/size
   - Growth potential
   - Remote flexibility

STEP 5 - FINAL OUTPUT:
Create a summary with:

TOP MATCHES (3-5 jobs):
For each, provide:
- Job Title | Company
- Match Score: X%
- Why it's a good fit: [key reasons]
- Salary: [if available]
- Link to job posting

DECENT FITS (next 5-10 jobs):
- Brief list with match scores and one-line summaries

NOT RECOMMENDED:
- Jobs with low match scores and why (skill gaps, unrealistic requirements)

KEY INSIGHTS:
- Common technologies I should learn
- Salary ranges observed
- Common experience requirements

IMPORTANT REMINDERS:
- Take your time - aim for 10-15 minutes total
- Don't click too fast or scroll too smoothly
- Vary your behavior to seem human
- If LinkedIn shows a CAPTCHA or asks for verification, pause and notify me
""",





"SEND_MESSAGE": """
OBJECTIVE: Find Hitesh Choudhary on LinkedIn and send him a message.

STEP 1 - SEARCH:
1. Go to https://www.linkedin.com/feed/
2. Click the search bar, type "Hitesh Choudhary", press Enter
3. Click the "People" filter tab and wait for results

STEP 2 - FIND PROFILE:
- Look for Hitesh Choudhary who is a YouTuber/educator with the highest follower count
- Click on his profile

STEP 3 - CHECK CONNECTION & MESSAGE:
Click the "More" (three dots ...) button near the Message button. A dropdown appears:

- If dropdown shows "Remove connection" → click the Message button and send: "Hi sir"
- If dropdown shows "Pending" → stop, report: "Connection request already pending"
- If dropdown shows "Connect" → stop, report: "Not connected"

STEP 4 - OUTPUT:
Report:
- Connection status found: [Connected / Pending / Not Connected]
- Action taken: [Message sent / No action]
- Message sent: "Hi sir" (Yes/No)
""",


  "IS_FOLLOWING": """
Go to LinkedIn and check the follow status of Utkarsh Deoli.


STEPS:
1. Click the search bar at the top of the LinkedIn page
2. Type "Utkarsh Deoli" and press Enter
3. When results load, click the "People" filter tab
4. Find "Utkarsh Deoli" from "Crux Sphere Technology" and open his profile
5. Check the current follow status:

   IF "Follow" button is visible (not following):
   return "Not following"

   IF "Follow" button is not visible (already following):
    return "already following"

BACKUP (if search bar fails):
1. Navigate directly to: https://www.linkedin.com/search/results/people/?keywords=Utkarsh%20Deoli
2. Click the "People" filter tab
3. Find "Utkarsh Deoli" from "Crux Sphere Technology" and open his profile
4. Follow the same steps from step 5 above


STOP IF:
- Login page appears → "Session expired"
- Profile not found after both methods → "Profile not found"
- CAPTCHA appears → "CAPTCHA detected"
""",



  "FOLLOW_PERSON": """
GOAL: Follow Utkarsh Deoli on LinkedIn.

STEP 1 — SEARCH
Click the LinkedIn search bar at the top.
Type: Utkarsh Deoli Crux Sphere Technology
Press Enter. Wait 3 seconds.

STEP 2 — FILTER BY PEOPLE
Click the "People" tab near the top of results.
Wait 3 seconds.
If "People" tab not visible → click "See all results" first, then "People".

STEP 3 — FIND CORRECT PROFILE
For each result card, check:
  ✓ Name matches "Utkarsh Deoli"
  ✓ Tagline/subtitle mentions "Crux Sphere Technology"
If both match → proceed to STEP 4.
If no match on first page → scroll down 300px, wait 2 seconds, repeat.
After 3 scrolls with no match → report "Profile not found" and stop.

STEP 4 — OPEN PROFILE
Click on "Utkarsh Deoli" in the matched result card.
Wait 4 seconds for page to load.
Verify:
  ✓ URL contains "/in/"
  ✓ Name shows "Utkarsh Deoli"
  ✓ Company shows "Crux Sphere Technology"
If verification fails → go back and try next matching card.

STEP 5 — FOLLOW
Check the profile buttons:

IF "Follow" button is visible:
  → Click "Follow"
  → Wait 2 seconds
  → Confirm button changed to "Following"
  → STOP. Go to output.

IF "Follow" button is NOT visible (already following):
  → Do NOT unfollow
  → STOP. Go to output with status "Already following".

⚠️ Do not click any other buttons. One action only.

STEP 6 — OUTPUT
- Profile found: Yes / No
- Initial status: Following / Not following
- Action taken: Followed / Already following (no action needed)
- Final status: Following

STOP IF:
- Login page → report "Session expired"
- Profile not found → report "Profile not found"
- CAPTCHA → report "CAPTCHA detected"
""",


"UNFOLLOW_PERSON": """
GOAL: Unfollow Utkarsh Deoli on LinkedIn.

STEP 1 — SEARCH
Click the LinkedIn search bar at the top.
Type: Utkarsh Deoli Crux Sphere Technology
Press Enter. Wait 3 seconds.

STEP 2 — FILTER BY PEOPLE
Click the "People" tab near the top of results.
Wait 3 seconds.
If "People" tab not visible → click "See all results" first, then "People".

STEP 3 — FIND CORRECT PROFILE
For each result card, check:
  ✓ Name matches "Utkarsh Deoli"
  ✓ Tagline/subtitle mentions "Crux Sphere Technology"
If both match → proceed to STEP 4.
If no match on first page → scroll down 300px, wait 2 seconds, repeat.
After 3 scrolls with no match → report "Profile not found" and stop.

STEP 4 — OPEN PROFILE
Click on "Utkarsh Deoli" in the matched result card.
Wait 4 seconds for page to load.
Verify:
  ✓ URL contains "/in/"
  ✓ Name shows "Utkarsh Deoli"
  ✓ Company shows "Crux Sphere Technology"
If verification fails → go back and try next matching card.

STEP 5 — UNFOLLOW
Check the profile buttons:

IF "Follow" button is visible (not following):
  → Do NOT follow
  → STOP. Go to output with status "Already not following".

IF "Follow" button is NOT visible (currently following):
  → Click the "..." (More) button next to the "Message" button
  → Wait 1 second for dropdown
  → Click "Unfollow" in the dropdown
  → If confirmation modal appears → click "Unfollow" to confirm
  → Wait 2 seconds
  → Confirm button changed back to "Follow"
  → STOP. Go to output.

⚠️ Do not click any other buttons. One action only.

STEP 6 — OUTPUT
- Profile found: Yes / No
- Initial status: Following / Not following
- Action taken: Unfollowed / Already not following (no action needed)
- Final status: Not following

STOP IF:
- Login page → report "Session expired"
- Profile not found → report "Profile not found"
- CAPTCHA → report "CAPTCHA detected"
""",



"LIKE_POST": """
Go to LinkedIn and like the most recent post by Hitesh Choudhary.

STEPS:
1. Click the search bar at the top of the LinkedIn page
2. Type "Hitesh Choudhary" and press Enter
3. When results load, click the "People" filter tab
4. Find "Hitesh Choudhary" . he is a you tuber  and open his profile
5. On his profile, click the "Posts" tab to see his posts
6. Find the first/most recent post
7. Check the Like button status:
   - IF the Like (thumbs up) button is NOT already liked → click it → confirm it turns blue/active
   - IF the Like button is already liked/active → report "Post already liked"
8. Report result clearly



OUTPUT FORMAT:
- Profile found: Yes / No
- Post found: Yes / No
- Post content preview: [first 10 words of the post]
- Like status before: Liked / Not liked
- Action taken: Clicked Like / No action needed
- Result: Successfully liked / Already liked / Failed to like

STOP IF:
- Login page appears → "Session expired"
- Profile not found after both methods → "Profile not found"
- No posts found on profile → "No posts found"
- CAPTCHA appears → "CAPTCHA detected"
""",




"COMMENT_POST": """
You are a browser automation agent.

GOAL: Find Hitesh Choudhary on LinkedIn, open his most recent post, and comment "Nice content" on it.

========================================
STEP 1 — SEARCH
========================================
Click the search bar at the top of the LinkedIn page.
Type: Hitesh Choudhary
→ Press Enter. Wait 2 seconds.

Click the "People" filter tab. Wait 2 seconds.

========================================
STEP 2 — FIND CORRECT PROFILE
========================================
Look through results for "Hitesh Choudhary".
He is a YouTuber — his tagline will mention YouTube, coding, or teaching.

If found → click his name to open profile. Wait 4 seconds.
If not found → scroll 300px, wait 2 seconds, repeat up to 3 times.
After 3 scrolls with no match → report "Profile not found" and STOP.

========================================
STEP 3 — OPEN POSTS TAB
========================================
On his profile page, find the "Posts" tab (usually below the ACTIVITY section).
Click it. Wait 3 seconds for posts to load.

If "Posts" tab not visible → scroll down slightly to reveal it.

========================================
STEP 4 — FIND MOST RECENT POST
========================================
The first post visible at the top is the most recent.

Do NOT click into the post yet.

========================================
STEP 5 — CHECK COMMENT BOX
========================================
Below the post, find the Comment input area.
It usually says "Add a comment..." as placeholder text.

IF the comment box is directly visible:
  → Click inside it. Wait 1 second. Proceed to STEP 6.

IF the comment box is not visible:
  → Click the Comments icon (speech bubble icon) below the post.
  → Wait 1 second for comment box to appear.
  → Click inside the comment box. Proceed to STEP 6.

========================================
STEP 6 — TYPE AND SUBMIT COMMENT
========================================
Type exactly:
Nice content

Wait 1 second after typing.

Look for the "Comment"  button near the comment box.
Click it to submit the comment.
Wait 2 seconds to confirm submission.

⚠️ Do NOT press Enter to submit — it may add a new line instead.
Use the 'Comment' button only.

STOP IMMEDIATELY after submitting.
Do not click anything else.

========================================
STEP 7 — OUTPUT
========================================
Return exactly this format:

- Profile found: Yes / No
- Post found: Yes / No
- Post content preview: [first 10 words of the post]
- Action taken: Commented / Failed to comment
- Comment text: "Nice content"
- Result: Successfully commented / Failed to comment

========================================
STOP CONDITIONS
========================================
- Login page → "Session expired"
- Profile not found → "Profile not found"
- No posts found → "No posts found"
- CAPTCHA → "CAPTCHA detected"
- Any error → report what you have and STOP
""",



}