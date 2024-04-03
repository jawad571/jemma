import jemma_utils as ju
from enum import Enum
import pandas as pd

class Metrics(Enum):
	NUMBER_OF_CLASSES_IN_PROJECT="number_of_classes_in_project"
	NUMBER_OF_PARAMETERS="number_of_parameters"
	NUMBER_OF_METHODS="number_of_methods"

method_parameters = "./jemma_datasets/properties/Jemma_Properties_Methods_NMPR.csv"
method_parameters_df = pd.read_csv(method_parameters)

classes = "./jemma_datasets/metadata/Jemma_Metadata_Classes.csv"
classes_df = pd.read_csv(classes)
classes_counts = classes_df.value_counts("project_id")

methods = "./jemma_datasets/metadata/Jemma_Metadata_Methods.csv"
methods_df = pd.read_csv(methods)
methods_counts = methods_df.value_counts("project_id")

projects = "./jemma_datasets/metadata/Jemma_Metadata_Projects.csv"
projects_df = pd.read_csv(projects)

def extract_metrics_from_project(project_id):
	metrics = {
		Metrics.NUMBER_OF_CLASSES_IN_PROJECT.value: classes_counts[project_id],
		Metrics.NUMBER_OF_METHODS.value: methods_counts[project_id],
		Metrics.NUMBER_OF_PARAMETERS.value: 0
	}

	methods_in_project = methods_df.loc[methods_df['project_id'] == project_id]["method_id"]
	for method_id in methods_in_project:
		print(method_id)
		metrics[Metrics.NUMBER_OF_PARAMETERS.value] = metrics[Metrics.NUMBER_OF_PARAMETERS.value] + int(method_parameters_df.loc[method_parameters_df["method_id"] == method_id, ['num_parameters']]['num_parameters'][0])
	return metrics



# columns = [
# 	Metrics.NUMBER_OF_CLASSES_IN_PROJECT.value,
# 	Metrics.NUMBER_OF_METHODS.value,
# 	Metrics.NUMBER_OF_PARAMETERS.value
# ]
# rows = []
# for project_id in projects_df['project_id']:
# 	print(f'Extracting insights for project {project_id}')
# 	metrics = extract_metrics_from_project(project_id)
# 	rows.append([
# 		metrics[Metrics.NUMBER_OF_CLASSES_IN_PROJECT.value],
# 		metrics[Metrics.NUMBER_OF_METHODS.value],
# 		metrics[Metrics.NUMBER_OF_PARAMETERS.value]
#     ])

# consolidated_metrics_df = pd.DataFrame(rows, columns=columns)
# consolidated_metrics_df.to_csv("50kc_insights.csv")
# print(consolidated_metrics_df)

all_methods = ju.get_project_method_ids("dfafb6b5-8461-4c05-9fd5-facae04d7967")
method_properties = ju.get_properties('NMPR',all_methods)
print(method_properties['num_parameters'].sum())
