_go_dotfiles = 'cd $HOME/dotfiles'
_dc_command = f'$({_go_dotfiles} && poetry run which dc)'

commands = dict(
    # dfc commands
    dc=dict(
        description='The dotfiles cli',
        command=f"""
            {_dc_command} $@
        """
    ),
    dcs=dict(
        description='Search commands and aliases (prints the command name)',
        command="""
            dc list | fzf --delimiter='\\0' --with-nth=1,2 | awk -F'\\0' '{{print $1}}'
        """
    ),
    dcw=dict(
        description='Search commands and aliases (prints the linked command)',
        command="""
            dc list | fzf --delimiter='\\0' --with-nth=1,2 | awk -F'\\0' '{{print $3}}'
        """
    ),
    dcr=dict(
        description='Run commands and aliases',
        command="""
            eval `dcw`
        """
    ),

    # dc global variants
    dcg=dict(
        description='The dotfiles cli (global)',
        command=f"""
            dc -g $@
        """
    ),
    dcsg=dict(
        description='Search commands and aliases (prints the command name) (global)',
        command=f"""
            dc -g list | fzf --delimiter='\\0' --with-nth=1,2 | awk -F'\\0' '{{print $1}}'
        """
    ),
    dcwg=dict(
        description='Search commands and aliases (prints the linked command) (global)',
        command=f"""
            dc -g list | fzf --delimiter='\\0' --with-nth=1,2 | awk -F'\\0' '{{print $3}}'
        """
    ),
    dcrg=dict(
        description='Run commands and aliases (global)',
        command="""
            eval `dcwg`
        """
    ),

)
