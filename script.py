from mestDS.mestDS import mestDS

_mestds = mestDS("example-dsl.yaml")  # Initialize mestDS with dsl
sims = _mestds.simulate()  # simulate data based on dsl definitions
_mestds.evaluate(sims)  # evaluate models defined in dsl on the simulated data
