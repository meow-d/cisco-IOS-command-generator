# networking script generator
>generates cisco IOS commands to setup subnets, DHCP, and RIP

- ideal for lazy students who don't want to go through this tedious process manually

## features
- automatically calculates subnet, network address, and ip addresses based on number of hosts needed
- generates cisco IOS commands to setup subnets, DHCP, and RIP

## installation
- download the project
  - `git clone https://github.com/meow-d/cisco-IOS-command-generator`
- install required packages
  - `pip install -r requirements.txt`
  - or `pip install lxml Markdown pandas`

## usage
1. manually edit the python if your questions demand something specific
2. fill in the input table
   1. use whatever tool you want to fill in the markdown table
      1. for example: VScode, with the `markdown all in one` and `Markdown Table` extensions
   2. fill in the table
      - `name` - name of each network
      - `type` - if the network is between routers, or for a group of computers connected through a switch
      - `hosts` - the number of hosts needed
      - `in/out_port/device` - the devices and ports. only `router` networks need `in_port/device`
3. run
   1. example: `python -u main.py input_table.md`
4. manually edit the generated script yourself. see limitations below
5. copy and paste into each device
   1. protip: if you can't use `ctrl-v`, use `rightclick+uparrow`. super fast if you have a right click key on your keyboard

## limitations (important!)
will probably never fix because i'm done with this module
- [ ] switch and router sections are seperate, meaning there are two subsections for each device. ideally each device should get one subsection with all of its commands
- [ ] lack of flexibility. your question will almost always require you to do something different, which often requires you to change the commands manually.
- [ ] duplicate code between the two sections
- [ ] inefficient RIP configuration
  - it's not very effieient to keep exiting
  - in the example, routerABC doesn't have any rip configuration in the router section

## License
Distributed under the MIT license. See ``LICENSE`` for more information.

## Contributing
1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

