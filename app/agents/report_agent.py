import os


class ReportAgent:

    def run(self, state):

        print(
            "\nReport Agent Running..."
        )

        research = state.get(
            "research",
            {}
        )

        verification = state.get(
            "verification",
            {}
        )

        roadmap = state.get(
            "roadmap",
            []
        )

        report = []

        report.append("=" * 60)

        report.append(
            f"PLACEMENT PREPARATION REPORT - "
            f"{state['company']}"
        )

        report.append("=" * 60)

        # =====================
        # Research
        # =====================

        report.append(
            "\nRESEARCH FINDINGS"
        )

        report.append("-" * 30)

        report.append(
            f"\nCompany: "
            f"{research.get('company', state['company'])}"
        )

        report.append(
            "\n\nDSA Topics:"
        )

        for topic in research.get(
            "dsa_topics",
            []
        ):

            report.append(
                f"  • {topic}"
            )

        report.append(
            "\n\nCS Subjects:"
        )

        for subject in research.get(
            "cs_subjects",
            []
        ):

            report.append(
                f"  • {subject}"
            )

        report.append(
            f"\n\nOA Pattern: "
            f"{research.get('oa_pattern', 'N/A')}"
        )

        report.append(
            f"\nInterview Rounds: "
            f"{research.get('interview_rounds', 'N/A')}"
        )

        report.append(
            f"\nSalary Range: "
            f"{research.get('salary_range', 'N/A')}"
        )

        # =====================
        # Verification
        # =====================

        report.append(
            "\n\nVERIFICATION REPORT"
        )

        report.append("-" * 30)

        report.append(
            f"\nStatus: "
            f"{verification.get('status', 'Unknown')}"
        )

        report.append(
            f"\nConfidence Score: "
            f"{verification.get('confidence', 0)}%"
        )

        # =====================
        # Roadmap
        # =====================

        report.append(
            "\n\nPREPARATION ROADMAP"
        )

        report.append("-" * 30)

        for phase in roadmap:

            if isinstance(
                phase,
                dict
            ):

                report.append(
                    f"\n{phase.get('phase', '')}"
                )

                report.append(
                    f"Days: "
                    f"{phase.get('days', '')}"
                )

                topics = phase.get(
                    "topics",
                    []
                )

                for topic in topics:

                    report.append(
                        f"   • {topic}"
                    )

        final_report = "\n".join(
            report
        )

        os.makedirs(
            "app/output/reports",
            exist_ok=True
        )

        file_path = (
            f"app/output/reports/"
            f"{state['company']}_Report.txt"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                final_report
            )

        state["report"] = (
            final_report
        )

        print(
            f"Report saved: {file_path}"
        )

        return state