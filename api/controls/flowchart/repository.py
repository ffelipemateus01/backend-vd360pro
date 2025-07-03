from api.controls.flowchart.models import Flowchart

def save_flowchart(flowchart: Flowchart):
    try:
        jflow = flowchart.model_dump_json()
        with open('flowchart.json', 'w', encoding='utf-8') as archive:
            archive.write(jflow)
    except Exception as e:
        raise ValueError()