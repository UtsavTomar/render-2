import sys
# from markdown_pdf import MarkdownPdf, Section
from crewai_enterprise_content_marketing_ideas.crew import CrewaiEnterpriseContentMarketingCrew


def run():
    """
    Run the crew.
    """
    # apikeys_dict = apikeys
    # for i in apikeys_dict.keys():
    #     globals()[i] = apikeys_dict[i]

    inputs = {'topic': 'AI Agent Framework', 'company': 'CrewAI'}
    CrewaiEnterpriseContentMarketingCrew().crew().kickoff(inputs=
        inputs)
    # pdf = MarkdownPdf(toc_level=1)
    # pdf.add_section(Section(result.raw))
    # pdf.save(f"{inputs['lead_info']['company']}_sales_pdf.pdf")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {'topic': 'AI Agent Framework', 'company': 'CrewAI'}
    try:
        CrewaiEnterpriseContentMarketingCrew().crew().train(n_iterations=
            int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f'An error occurred while training the crew: {e}')


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CrewaiEnterpriseContentMarketingCrew().crew().replay(task_id=sys.
            argv[1])
    except Exception as e:
        raise Exception(f'An error occurred while replaying the crew: {e}')


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {'topic': 'AI Agent Framework', 'company': 'CrewAI'}
    try:
        CrewaiEnterpriseContentMarketingCrew().crew().test(n_iterations=int
            (sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f'An error occurred while replaying the crew: {e}')




def run_main(inputs,apikeys):
    input_data = inputs if inputs is not None else {}
    return run(input_data,apikeys)
