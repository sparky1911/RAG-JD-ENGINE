const analyzeBtn =
    document.getElementById(
        "analyzeBtn"
    );

const resultDiv =
    document.getElementById(
        "result"
    );

const loadingDiv =
    document.getElementById(
        "loading"
    );

const textarea =
    document.getElementById(
        "jobDescription"
    );


function renderResult(data) {

    resultDiv.innerHTML = `
        <div class="score">
            Match Score: ${data.score}%
        </div>

        <div class="section-title">
            Matched Skills
        </div>

        ${
            data.matched_skills
                .map(
                    skill =>
                        `<div class="skill">
                            ✅ ${skill}
                        </div>`
                )
                .join("")
        }

        <div class="section-title">
            Missing Skills
        </div>

        ${
            data.missing_skills
                .map(
                    skill =>
                        `<div class="skill">
                            ❌ ${skill}
                        </div>`
                )
                .join("")
        }

        <div class="section-title">
            Summary
        </div>

        <div>
            ${data.summary}
        </div>
    `;
}


analyzeBtn.addEventListener(
    "click",
    async () => {

        const jobDescription =
            textarea.value.trim();

        if (!jobDescription) {

            resultDiv.innerHTML =
                "Please paste a job description.";

            return;
        }

        loadingDiv.style.display =
            "block";

        resultDiv.innerHTML = "";

        try {

            const response =
                await fetch(
                    "http://127.0.0.1:8000/analyze-job",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            job_description:
                                jobDescription
                        })
                    }
                );

            const data =
                await response.json();

            loadingDiv.style.display =
                "none";

            renderResult(
                data.result
            );

        } catch (error) {

            loadingDiv.style.display =
                "none";

            resultDiv.innerHTML =
                "Backend connection failed.";
        }
    }
);