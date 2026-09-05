// ==========================================================================
// AI Placement Preparation Agent - Frontend Client Script
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("agent-form");
    const companyInput = document.getElementById("company-input");
    const daysSelect = document.getElementById("days-select");
    const submitBtn = document.getElementById("submit-btn");
    const quickTags = document.querySelectorAll(".quick-tag");

    const errorSection = document.getElementById("error-section");
    const errorTitle = document.getElementById("error-title");
    const errorDesc = document.getElementById("error-desc");

    const progressSection = document.getElementById("progress-section");
    const progressStatusTitle = document.getElementById("progress-status-title");
    const progressStatusDesc = document.getElementById("progress-status-desc");
    const stepCards = [
        document.getElementById("step-1"),
        document.getElementById("step-2"),
        document.getElementById("step-3"),
        document.getElementById("step-4"),
        document.getElementById("step-5")
    ];


    const resultsSection = document.getElementById("results-section");
    const resultCompanyName = document.getElementById("result-company-name");
    const resultDaysBadge = document.getElementById("result-days-badge");
    const resultConfidenceBadge = document.getElementById("result-confidence-badge");
    const resultDifficultyBadge = document.getElementById("result-difficulty-badge");
    const downloadPptBtn = document.getElementById("download-ppt-btn");
    const downloadReportBtn = document.getElementById("download-report-btn");

    const tabBtns = document.querySelectorAll(".tab-btn");
    const tabPanes = document.querySelectorAll(".tab-pane");

    const roadmapContainer = document.getElementById("roadmap-container");
    const slidesContainer = document.getElementById("slides-container");
    const intelContainer = document.getElementById("intel-container");
    const reportText = document.getElementById("report-text");
    const copyReportBtn = document.getElementById("copy-report-btn");
    const slideCount = document.getElementById("slide-count");

    let progressInterval = null;

    // Quick tag selector
    quickTags.forEach(tag => {
        tag.addEventListener("click", () => {
            companyInput.value = tag.getAttribute("data-company");
            companyInput.focus();
        });
    });

    // Tab switching
    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            tabBtns.forEach(b => b.classList.remove("active"));
            tabPanes.forEach(p => p.classList.remove("active"));

            btn.classList.add("active");
            const targetTab = document.getElementById(btn.getAttribute("data-tab"));
            if (targetTab) {
                targetTab.classList.add("active");
            }
        });
    });

    // Form Submission
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const company = companyInput.value.trim();
        const days = parseInt(daysSelect.value, 10) || 60;

        if (!company) {
            alert("Please enter a company name.");
            return;
        }

        // UI Transition to Loading State
        if (errorSection) errorSection.classList.add("hidden");
        submitBtn.disabled = true;
        submitBtn.querySelector(".btn-text").textContent = "Agents Running...";
        progressSection.classList.remove("hidden");
        resultsSection.classList.add("hidden");
        progressSection.scrollIntoView({ behavior: "smooth" });

        startProgressSimulation(company);

        try {
            const response = await fetch("/generate-ppt", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    company: company,
                    days: days
                })
            });

            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                throw new Error(errData.error || `Server returned ${response.status}`);
            }

            const data = await response.json();

            stopProgressSimulation(true);
            renderResults(data, company, days);

        } catch (error) {
            console.error("Agent Execution Error:", error);
            stopProgressSimulation(false);
            if (errorSection && errorTitle && errorDesc) {
                errorTitle.textContent = "Agent Execution Error";
                errorDesc.textContent = error.message || "Failed to generate report. Please try again or check server logs.";
                errorSection.classList.remove("hidden");
                errorSection.scrollIntoView({ behavior: "smooth" });
            } else {
                alert(`Error running agents: ${error.message || "Failed to generate report"}`);
            }
        } finally {
            submitBtn.disabled = false;
            submitBtn.querySelector(".btn-text").textContent = "Launch Placement Agents";
        }
    });

    // Simulated step progression for smooth UX while backend agents execute
    function startProgressSimulation(company) {
        let currentStep = 0;
        stepCards.forEach((card, idx) => {
            card.className = "step-card" + (idx === 0 ? " active" : "");
        });

        const stepDescriptions = [
            { title: "ResearchAgent Working...", desc: `Scraping recent online assessment patterns and interview data for ${company}.` },
            { title: "VerificationAgent Cross-Checking...", desc: `Validating interview question frequency and calculating confidence score.` },
            { title: "RoadmapAgent Formulating...", desc: `Drafting customized multi-phase study plan across DSA & CS core.` },
            { title: "SlideContentAgent Synthesizing...", desc: `Structuring 10 comprehensive slides for presentation deck.` },
            { title: "Report & PPT Synthesis...", desc: `Compiling final presentation and placement document.` }
        ];

        progressInterval = setInterval(() => {
            if (currentStep < 4) {
                stepCards[currentStep].classList.remove("active");
                stepCards[currentStep].classList.add("completed");

                currentStep++;
                stepCards[currentStep].classList.add("active");

                progressStatusTitle.textContent = stepDescriptions[currentStep].title;
                progressStatusDesc.textContent = stepDescriptions[currentStep].desc;
            }
        }, 6000);
    }

    function stopProgressSimulation(success) {
        if (progressInterval) {
            clearInterval(progressInterval);
            progressInterval = null;
        }

        if (success) {
            stepCards.forEach(card => {
                card.classList.remove("active");
                card.classList.add("completed");
            });
            setTimeout(() => {
                progressSection.classList.add("hidden");
            }, 600);
        } else {
            progressSection.classList.add("hidden");
        }
    }

    // Render Results on the Dashboard
    function renderResults(data, company, days) {
        resultsSection.classList.remove("hidden");

        // Top Banner
        resultCompanyName.textContent = `${company.toUpperCase()} Placement Guide`;
        resultDaysBadge.textContent = `${days} Days Roadmap`;

        const confidence = data.verification?.confidence ?? 85;
        resultConfidenceBadge.textContent = `Confidence: ${confidence}%`;
        if (confidence >= 70) {
            resultConfidenceBadge.className = "meta-pill green";
        } else {
            resultConfidenceBadge.className = "meta-pill purple";
        }

        const difficulty = data.company_profile?.difficulty || "Medium";
        resultDifficultyBadge.textContent = `Difficulty: ${difficulty}`;

        // Download Links
        downloadPptBtn.href = data.download_url || `/download-ppt/${company}`;
        downloadReportBtn.href = data.report_url || `/download-report/${company}`;

        // 1. Render Roadmap
        renderRoadmap(data.roadmap || []);

        // 2. Render Slides
        renderSlides(data.slide_content || []);

        // 3. Render Company Intelligence
        renderIntel(data.company_profile || {}, company);

        // 4. Render Report
        reportText.textContent = data.report || "No raw text report generated.";

        resultsSection.scrollIntoView({ behavior: "smooth" });
    }

    function renderRoadmap(roadmap) {
        roadmapContainer.innerHTML = "";
        if (!roadmap || roadmap.length === 0) {
            roadmapContainer.innerHTML = "<p class='subtext'>No roadmap phases available.</p>";
            return;
        }

        roadmap.forEach((phase) => {
            const card = document.createElement("div");
            card.className = "phase-card";

            const header = document.createElement("div");
            header.className = "phase-header";

            const title = document.createElement("h3");
            title.className = "phase-title";
            title.textContent = phase.phase || "Phase";

            const daysBadge = document.createElement("span");
            daysBadge.className = "phase-days";
            daysBadge.textContent = `Days: ${phase.days || "N/A"}`;

            header.appendChild(title);
            header.appendChild(daysBadge);

            const topicsDiv = document.createElement("div");
            topicsDiv.className = "phase-topics";

            const topics = phase.topics || [];
            topics.forEach(topic => {
                const topicTag = document.createElement("span");
                topicTag.className = "topic-tag";
                topicTag.textContent = topic;
                topicsDiv.appendChild(topicTag);
            });

            card.appendChild(header);
            card.appendChild(topicsDiv);
            roadmapContainer.appendChild(card);
        });
    }

    function renderSlides(slides) {
        slidesContainer.innerHTML = "";
        slideCount.textContent = slides.length || 0;

        if (!slides || slides.length === 0) {
            slidesContainer.innerHTML = "<p class='subtext'>No slides generated.</p>";
            return;
        }

        slides.forEach((slide, index) => {
            const card = document.createElement("div");
            card.className = "slide-item-card";

            const num = document.createElement("span");
            num.className = "slide-num";
            num.textContent = `Slide ${index + 1}`;

            const title = document.createElement("h4");
            title.className = "slide-title";
            title.textContent = slide.title || `Slide ${index + 1}`;

            const list = document.createElement("ul");
            list.className = "slide-bullets";

            const bullets = slide.content || [];
            bullets.forEach(bullet => {
                const li = document.createElement("li");
                li.textContent = bullet;
                list.appendChild(li);
            });

            card.appendChild(num);
            card.appendChild(title);
            card.appendChild(list);
            slidesContainer.appendChild(card);
        });
    }

    function renderIntel(profile, company) {
        intelContainer.innerHTML = "";

        const fields = [
            { label: "Company Name", value: profile.company_name || company },
            { label: "Industry", value: profile.industry || "Software & Technology" },
            { label: "Difficulty Level", value: profile.difficulty || "Medium" },
            { label: "Interview Style", value: profile.interview_style || "Technical Coding & System Design" },
            { label: "Primary Focus", value: profile.focus || "DSA, Problem Solving & Core CS" },
            { label: "Company Type", value: profile.company_type || "Product" }
        ];

        fields.forEach(f => {
            const card = document.createElement("div");
            card.className = "intel-card";
            card.innerHTML = `<h4>${f.label}</h4><p>${f.value}</p>`;
            intelContainer.appendChild(card);
        });

        // Special topics & strategies if present
        if (profile.special_topics && profile.special_topics.length > 0) {
            const card = document.createElement("div");
            card.className = "intel-card";
            card.innerHTML = `<h4>Special Focus Topics</h4><ul class="intel-list">${profile.special_topics.map(t => `<li>${t}</li>`).join("")}</ul>`;
            intelContainer.appendChild(card);
        }

        if (profile.preparation_strategy && profile.preparation_strategy.length > 0) {
            const card = document.createElement("div");
            card.className = "intel-card";
            card.innerHTML = `<h4>Preparation Strategy</h4><ul class="intel-list">${profile.preparation_strategy.map(s => `<li>${s}</li>`).join("")}</ul>`;
            intelContainer.appendChild(card);
        }
    }

    // Copy report
    copyReportBtn.addEventListener("click", () => {
        if (!reportText.textContent) return;
        navigator.clipboard.writeText(reportText.textContent).then(() => {
            const originalText = copyReportBtn.textContent;
            copyReportBtn.textContent = "? Copied!";
            setTimeout(() => {
                copyReportBtn.textContent = originalText;
            }, 2000);
        }).catch(err => {
            console.error("Clipboard error:", err);
        });
    });
});
