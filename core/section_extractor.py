class SectionExtractor:

    HEADERS = [
        "WORK EXPERIENCE",
        "EXPERIENCE",
        "EDUCATION",
        "PROJECTS",
        "PERSONAL PROJECTS",
        "TECHNICAL SKILLS",
        "SKILLS",
        "CERTIFICATES",
        "CERTIFICATIONS"
    ]

    @staticmethod
    def extract_all_sections(text):

        text_upper = text.upper()

        positions = {}

        for header in SectionExtractor.HEADERS:

            idx = text_upper.find(header)

            if idx != -1:
                positions[header] = idx

        sorted_headers = sorted(positions.items(), key=lambda x: x[1])

        sections = {}

        for i, (header, start) in enumerate(sorted_headers):

            end = len(text)

            if i + 1 < len(sorted_headers):
                end = sorted_headers[i+1][1]

            sections[header] = text[start:end]

        return {
            "work_experience":
                sections.get("WORK EXPERIENCE") or sections.get("EXPERIENCE") or "",
            "education":
                sections.get("EDUCATION") or "",
            "projects":
                sections.get("PROJECTS") or sections.get("PERSONAL PROJECTS") or "",
            "skills":
                sections.get("TECHNICAL SKILLS") or sections.get("SKILLS") or ""
        }
