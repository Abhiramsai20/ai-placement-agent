from app.services.llm_service import LLMService

from app.prompts.slide_content_prompt import (
    SLIDE_CONTENT_PROMPT
)

from app.utils.slide_json_parser import (
    extract_slide_json
)


class SlideContentAgent:

    def __init__(self):

        self.llm = LLMService()

    def run(self, state):

        print(
            "\nSlide Content Agent Running..."
        )

        company = state["company"]

        research = state.get(
            "research",
            {}
        )

        profile = state.get(
            "company_profile",
            {}
        )

        roadmap = state.get(
            "roadmap",
            []
        )

        interview_experiences = state.get(
            "interview_experiences",
            []
        )

        days = state["days"]

        # Build prompt safely
        prompt = SLIDE_CONTENT_PROMPT

        prompt = prompt.replace(
            "{company}",
            str(company)
        )

        prompt = prompt.replace(
            "{profile}",
            str(profile)
        )

        prompt = prompt.replace(
            "{research}",
            str(research)
        )

        prompt = prompt.replace(
            "{roadmap}",
            str(roadmap)
        )

        prompt = prompt.replace(
            "{interview_experiences}",
            str(interview_experiences)
        )

        prompt = prompt.replace(
            "{days}",
            str(days)
        )

        print(
            "\nPROMPT CREATED SUCCESSFULLY"
        )

        response = self.llm.generate(
            prompt
        )

        print(
            "\nLLM RESPONSE RECEIVED"
        )

        try:

            slides = extract_slide_json(
                response
            )

            if not slides or len(slides) == 0:
                raise ValueError("Parsed slide list is empty")

            state["slide_content"] = (
                slides
            )

            print(
                f"Generated {len(slides)} slides"
            )

            for slide in slides:

                print(
                    f"✓ {slide.get('title')}"
                )

        except Exception as e:

            print(
                f"Slide Parse Failed: {e}. Generating fallback slides from research data..."
            )

            fallback_slides = self._generate_fallback_slides(state, company, days)
            state["slide_content"] = fallback_slides

            print(
                f"Synthesized {len(fallback_slides)} fallback slides successfully"
            )

        return state

    def _generate_fallback_slides(self, state, company, days):
        research = state.get("research", {})
        profile = state.get("company_profile", {})
        roadmap_raw = state.get("roadmap", [])
        if isinstance(roadmap_raw, dict):
            roadmap = []
            for k in ["phases", "roadmap", "schedule", "data"]:
                if k in roadmap_raw and isinstance(roadmap_raw[k], list):
                    roadmap = roadmap_raw[k]
                    break
            if not roadmap:
                roadmap = [v for v in roadmap_raw.values() if isinstance(v, (dict, list, str))]
        elif isinstance(roadmap_raw, list):
            roadmap = roadmap_raw
        else:
            roadmap = []

        # Extract DSA topics
        dsa_items = []
        for d in research.get("dsa_topics", []):
            if isinstance(d, dict):
                dsa_items.append(f"{d.get('topic', 'DSA')}: {', '.join(d.get('questions', [])[:2])}")
            elif isinstance(d, str):
                dsa_items.append(d)
        if not dsa_items:
            dsa_items = [
                "Arrays & Strings (Two Pointers, Sliding Window)",
                "Trees & Binary Search Trees (LCA, Traversals)",
                "Dynamic Programming (Knapsack, Subsequences)",
                "Graphs (BFS, DFS, Shortest Path)"
            ]

        # Extract CS subjects
        cs_items = []
        for c in research.get("cs_subjects", []):
            if isinstance(c, dict):
                cs_items.append(f"{c.get('subject', 'CS')}: {', '.join(c.get('important_topics', [])[:2])}")
            elif isinstance(c, str):
                cs_items.append(c)
        if not cs_items:
            cs_items = [
                "Database Management Systems (Normalization, Indexing)",
                "Operating Systems (Process Scheduling, Deadlocks)",
                "Computer Networks (TCP/IP, HTTP, DNS)",
                "Object Oriented Programming (Encapsulation, SOLID)"
            ]

        # Extract tips
        tips = research.get("preparation_tips", [])
        if not tips:
            tips = [
                f"Practice {company} tagged questions consistently on LeetCode",
                "Focus on edge cases and discuss space-time complexity",
                "Revise core CS subjects and prepare clear project narratives",
                "Participate in timed mock assessments"
            ]

        # Roadmap summary
        roadmap_items = []
        for p in roadmap[:4]:
            if isinstance(p, dict):
                roadmap_items.append(f"{p.get('phase', 'Phase')} ({p.get('days', '')}): {', '.join(p.get('topics', [])[:3])}")
        if not roadmap_items:
            roadmap_items = [
                f"Phase 1 (Days 1-{days//4}): Core DSA Foundation & Problem Solving",
                f"Phase 2 (Days {days//4 + 1}-{days//2}): Advanced Algorithms & Trees/Graphs",
                f"Phase 3 (Days {days//2 + 1}-{days*3//4}): Core CS Subjects & System Design",
                f"Phase 4 (Days {days*3//4 + 1}-{days}): Mock Assessments & Final Revision"
            ]

        return [
            {
                "title": "Company Overview",
                "content": [
                    f"{company} hiring and placement overview",
                    f"Industry: {profile.get('industry', 'Software & Technology')}",
                    f"Company Type: {profile.get('company_type', 'Product')}",
                    f"Difficulty: {profile.get('difficulty', 'Medium to Hard')}",
                    f"Interview Style: {profile.get('interview_style', 'Technical & Algorithmic')}"
                ]
            },
            {
                "title": "Hiring Process",
                "content": [
                    "Round 1: Resume Shortlisting & Screening",
                    "Round 2: Online Assessment (Coding & MCQs)",
                    "Round 3: Technical Coding Interview 1 (DSA)",
                    "Round 4: Technical Interview 2 (System Design & Projects)",
                    "Round 5: HR / Behavioral Leadership Round"
                ]
            },
            {
                "title": "Online Assessment Pattern",
                "content": [
                    f"Platform: Hackerrank / CodeSignal / Mettle",
                    f"Duration: 70 - 90 Minutes",
                    f"Questions: 2 - 3 Medium-Hard Coding Problems",
                    f"Core Topics: Arrays, Strings, Dynamic Programming",
                    f"Key Advice: Test edge cases and optimize time complexity"
                ]
            },
            {
                "title": "Important DSA Topics",
                "content": dsa_items[:6]
            },
            {
                "title": "Important CS Subjects",
                "content": cs_items[:6]
            },
            {
                "title": "Most Asked Interview Questions",
                "content": [
                    "Two Sum and 3Sum subarray problems",
                    "LRU Cache design using Doubly Linked List & Map",
                    "Binary Tree Level Order Traversal & Lowest Common Ancestor",
                    "Graph cycle detection and shortest path algorithm",
                    "String anagrams and palindrome partitioning"
                ]
            },
            {
                "title": "Salary And Career Growth",
                "content": [
                    f"Competitive salary package for SDE roles at {company}",
                    "Structured promotion tracks from SDE-1 to SDE-2 and Staff",
                    "Hands-on ownership of high-impact engineering projects",
                    "Comprehensive medical, wellness, and learning allowances",
                    "Culture emphasizing innovation and technical excellence"
                ]
            },
            {
                "title": f"{days}-Day Preparation Roadmap",
                "content": roadmap_items[:5]
            },
            {
                "title": "Best Resources",
                "content": [
                    f"LeetCode: Top {company} tagged questions",
                    "Striver SDE Sheet & NeetCode 150 for algorithm mastery",
                    f"GeeksforGeeks: Recent {company} interview experiences",
                    "Grokking Modern System Design for architecture interviews",
                    "Pramp & InterviewBit for peer mock interviews"
                ]
            },
            {
                "title": "Final Preparation Tips",
                "content": tips[:6]
            }
        ]