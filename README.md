# fast-rl-vn
Fast Reinforcement Learning with Prior Policy for Visual Navigation

## Enable/Disable Sim Logging
To turn off non-critical logging, use one of the following based on your current version:

Habitat-Sim version >= 0.2.2:
`export MAGNUM_LOG=quiet HABITAT_SIM_LOG=quiet`

Habitat-Sim version < 0.2.2:
`export MAGNUM_LOG=quiet GLOG_minloglevel=2`


## Scripts
1. Determine horizon and performance of a given agent to be used as guide
`python `

