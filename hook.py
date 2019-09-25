import asyncio
from random import randint

from plugins.mock.app.mock_svc import MockService

name = 'Mock'
description = 'Simulated agents for testing operations with no external dependencies'
address = None


async def initialize(app, services):
    await services['data_svc'].load_data(schema='plugins/%s/mock.sql' % name.lower())
    simulation_svc = MockService(services)
    simulated_responses = [r for r in services.get('agent_svc').strip_yml('plugins/%s/conf/responses.yml' % name.lower())[0]]
    await simulation_svc.load_simulation_results(simulated_responses)
    all_agents = [a for a in services.get('agent_svc').strip_yml('plugins/%s/conf/config.yml' % name.lower())[0]]
    await simulation_svc.set_agent_listing(all_agents)
    agents = [a for a in all_agents if 'expansion' not in a]
    loop = asyncio.get_event_loop()
    for a in agents:
        a['pid'], a['ppid'], a['sleep'] = randint(1000,10000), randint(1000, 10000), randint(55, 65)
        a['architecture'] = None
        a['server'] = 'http://localhost:8888'
        loop.create_task(simulation_svc.run(a))
