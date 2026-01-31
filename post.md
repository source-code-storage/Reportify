🚀 My Kiro Hackathon Journey: From Internship Struggles to Reportify






Liaichi Mustapha

Hackathon Participan...
5d

I spent two years solving the same problems over and over. Then one client came back for more, and I finally asked the obvious question.
Hey everyone! 👋

I just submitted my project for the Kiro Hackathon, and I wanted to share my journey with this amazing community. This has been one of the most rewarding experiences, and I owe a huge thanks to so many people here.

💡 Where It All Started

Let me take you back to my 6-month internship at LEAR as an AI Engineer. Amazing projects, incredible learning, but one persistent problem haunted me:

Week 1: "I'll remember this meeting about the project requirements."  

Week 8: "Wait, what did we decide in that first meeting?"  

Week 20: "I have no idea what I did in month one anymore."

The meetings. The random implementation notes. The tweaks. The context that made everything make sense. All scattered across notebooks, random text files, and my increasingly unreliable memory.

I tried everything:

- Overleaf? Not quite.

- Notion? Close, but no.

- Google Docs? Missing something.

- OneNote? Still not it.

Nothing gave me what I needed. And here's the kicke, I talked to my friends, and they ALL had this same problem. Every single intern, every junior developer, everyone starting something new.

🎯 The "Aha!" Moment

I'd been thinking about building something to solve this for months. I had the skills, the motivation, the problem... but between the internship workload and everything else, it never happened.

Then I saw Cole Medin's post about the https://dynamous.ai/#/kiro-hackathon .

It just clicked. 💡

I didn't have a project idea for the hackathon—I had a problem that had been chasing me for months. This was my chance to finally build something real, something that actually works.

That's how Reportify was born.



 🛠️ The Build Process (aka The Struggle Was Real)

Week 1: The Excitement Phase

"This is going to be easy! I'll have it done in a week!"

Narrator: It was not easy, and it was not done in a week.

Week 2: The Reality Check

- Vector databases? Never used Qdrant before.

- Semantic search? Sounds cool, but how do embeddings actually work?

- Celery task queues? Why is async processing so complicated?

- GPT-4 integration? Token limits are a thing?!

Week 3: The Breakthrough

This is where Kiro CLI became my best friend.

Instead of spending hours debugging why my Celery tasks weren't registering, Kiro helped me identify the issue in minutes. Instead of writing boilerplate code for 20+ API endpoints, Kiro generated clean, working code that I could build on.

Real talk: Kiro CLI saved me at least 27 hours of development time. I tracked it.

🎬 What I Built

Reportify - An AI-powered internship companion that:

📝 Smart Document Processing

- Upload PDFs, automatically extract sections

- OCR for scanned documents

- Template structure detection

🔍 Semantic Search

- Not just keyword matching—understands meaning

- Vector embeddings with Qdrant

- Find relevant info across all your notes

🤖 AI Content Generation

- GPT-4 powered content creation

- Context-aware generation from your notes

- Multiple generation modes

📤 Professional Export

- Export to PDF or DOCX

- Maintains formatting and structure

- Ready to submit

Tech Stack

- Backend: FastAPI, Python, PostgreSQL, Celery, Redis

- Frontend: React 18, TypeScript, Tailwind CSS, shadcn/ui

- AI: OpenAI GPT-4, Sentence Transformers, Qdrant

- Infrastructure: Docker, MinIO

💪 The Challenges (And How I Overcame Them)

 Challenge 1: Vector Search Was Returning Garbage

Problem: Qdrant was giving me completely irrelevant results.

Solution: Switched embedding models, tuned similarity thresholds from 0.5 to 0.7, added caching. Kiro CLI helped me understand the optimal configuration.

Lesson: Sometimes the default settings aren't the right settings.

Challenge 2: PDF Processing Blocked Everything

Problem: Large PDFs were timing out API requests.

Solution: Implemented Celery for async processing. Now uploads return immediately, and processing happens in the background.

Lesson: If it takes more than 2 seconds, make it async.

Challenge 3: GPT-4 Token Limits

Problem: "Error: Maximum context length exceeded" 😭

Solution: Smart chunking, context prioritization, token counting before API calls.

Lesson: AI is powerful, but you need to manage it carefully.

Challenge 4: "Why Isn't This Working?!"

Problem: Spent 2 hours debugging a Celery task registration issue.

Solution: Asked Kiro CLI. Got the answer in 5 minutes.

Lesson: Don't be afraid to ask for help (even from AI).

🎓 What I Learned

Technical Skills

- Vector databases and semantic search

- Async processing with Celery

- GPT-4 integration and prompt engineering

- Full-stack development with FastAPI + React

- Docker and deployment

 Soft Skills

- Breaking down complex problems

- Time management under deadlines

- Writing clear documentation

- Asking for help when stuck

- Celebrating small wins

The Big One

You don't need to have everything figured out before you start. 

I didn't know how to use Qdrant when I started. I'd never implemented semantic search. I'd barely touched Celery. But I learned as I built, and that's okay.

🙏 Thank You to This Amazing Community

Cole Medin - Thank you for introducing me to this hackathon. Without your post, Reportify wouldn't exist.

The Dynamous Team - Thank you for organizing this incredible hackathon and creating Kiro CLI. This tool is a game-changer.

Everyone who shared their projects - Seeing your builds inspired me to push harder and aim higher.

Everyone who answered questions - The community support here is incredible.

The Kiro CLI team - You built something special. Kiro didn't just help me code faster—it helped me learn faster.



🔗 Check It Out

GitHub: https://github.com/MuLIAICHI/Reportify  

The repo has:

- Complete source code

- Comprehensive documentation

- Setup instructions

- Demo video

- Architecture diagrams

💭 Final Thoughts

This hackathon taught me something important: The best projects come from real problems.

I didn't build Reportify because it sounded cool or because I wanted to win. I built it because I genuinely struggled with this problem during my internship, and I know others struggle with it too.

Whether I win or not, I'm proud of what I built. Reportify solves a real problem, and that's what matters.

🚀 To Everyone Still Building

If you're still working on your hackathon project:

You've got this! 💪

The deadline is close, but you can do it. Here's what helped me:

1. Focus on core features first - Polish can come later

2. Document as you go - Future you will thank present you

3. Test early and often - Don't wait until the last day

4. Ask for help - This community is amazing

5. Take breaks - Burnout helps no one

And remember: Done is better than perfect.

🎉 Let's Celebrate Together

No matter what happens with judging, we all built something. We all learned something. We all grew as developers.

That's worth celebrating. 🎊

To everyone who participated: You're awesome. Your projects are awesome. This community is awesome.

Let's keep building, keep learning, and keep supporting each other.



Thanks for reading my journey! Now go check out everyone else's amazing projects! 🚀

P.S. - If you're an intern or junior dev struggling with the same problem I had, give Reportify a try. That's literally why I built it. 😊

Built with ❤️, lots of ☕, and the incredible support of this community 
