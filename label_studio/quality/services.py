import json
from collections import Counter, defaultdict

from tasks.models import Annotation


def calculate_exact_match_agreement(project):
    annotations = (
        Annotation.objects.filter(project=project, was_cancelled=False)
        .exclude(result__isnull=True)
        .values('task_id', 'result')
    )

    by_task = defaultdict(list)
    for item in annotations:
        normalized = json.dumps(item['result'], ensure_ascii=False, sort_keys=True)
        by_task[item['task_id']].append(normalized)

    task_scores = []
    annotations_evaluated = 0
    for values in by_task.values():
        if len(values) < 2:
            continue
        annotations_evaluated += len(values)
        agreement = Counter(values).most_common(1)[0][1] / len(values)
        task_scores.append(agreement)

    score = round(sum(task_scores) / len(task_scores), 4) if task_scores else 1.0
    return {
        'metric': 'exact_match_consensus',
        'score': score,
        'tasks_evaluated': len(task_scores),
        'annotations_evaluated': annotations_evaluated,
    }
