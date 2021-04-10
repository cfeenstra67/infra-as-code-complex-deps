import argparse
import asyncio
import sys

import statey as st
from statey.ext.graphviz import get_graphviz_graph

import statey_conf
from statey_module import module


def task_filter(key, task):
    return not task.is_metatask() or type(task).__name__ == "SessionSwitch"


async def main(argv):
    parser = argparse.ArgumentParser("export_plan")
    parser.add_argument("output")

    args = parser.parse_args(argv)

    state_manager = st.registry.get_state_manager()
    resource_graph = state_manager.load(st.registry)

    session = st.create_resource_session()
    module(session)

    plan = await st.helpers.plan(session, resource_graph)

    gv_graph = get_graphviz_graph(
        plan.task_graph, task_filter=task_filter, format="svg"
    )
    gv_graph.render(args.output)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
