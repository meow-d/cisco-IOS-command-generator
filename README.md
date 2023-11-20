# networking script generator
generates cisco IOS commands to setup subnets, DHCP, and RIP

## features
- calculate subnet, network address and ip addresses
- generate cisco ios commands

## how to use
1. fill in the input table
   1. use whatever tool you want to fill in the markdown table
      1. for example: the `markdown all in one` extension from vscode
   2. fill in the table
      - `name` - name of each network
      - `type` - if the network is between routers, or for a group of computers connected through a switch
      - `hosts` - the number of hosts needed
      - `in/out_port/device` - the devices and ports. only `router` networks need `in_port/device`
2. run
   1. example: `python -u main.py input_table.md`
3. manually edit the generated script yourself. see limitations below
4. copy and paste into each device
   1. protip: if you can't use `ctrl-v`, use `rightclick+uparrow`. super fast if you have a right click key on your keyboard

## limitations
will probably never fix
- [ ] switch and router sections are seperate, meaning there are two subsections for each device. ideally each device should get one subsection with all of its commands
- [ ] lack of flexibility. your question will almost always require you to do something different, which often requires you to change the commands manually.
- [ ] duplicate code between the two sections
- [ ] inefficient RIP configuration
  - it's not very effieient to keep exiting
  - in the example, routerABC doesn't have any rip configuration in the router section
