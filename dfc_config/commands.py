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
    dc_search=dict(
        description='Search commands and aliases (prints the command name)',
        command="""
            dc list | fzf --delimiter='\\0' --with-nth=1,2 | awk -F'\\0' '{{print $1}}'
        """
    ),
    dc_search_target=dict(
        description='Search commands and aliases (prints the linked command)',
        command="""
            dc list | fzf --delimiter='\\0' --with-nth=1,2 | awk -F'\\0' '{{print $3}}'
        """
    ),
    dc_run=dict(
        description='Run commands and aliases',
        command="""
            eval `dc_search_target`
        """
    ),

    # dc global variants
    dcg=dict(
        description='The dotfiles cli (global)',
        command=f"""
            dc -g $@
        """
    ),
    dc_search_global=dict(
        description='Search commands and aliases (prints the command name) (global)',
        command=f"""
            dc -g list | fzf --delimiter='\\0' --with-nth=1,2 | awk -F'\\0' '{{print $1}}'
        """
    ),
    dc_search_target_global=dict(
        description='Search commands and aliases (prints the linked command) (global)',
        command=f"""
            dc -g list | fzf --delimiter='\\0' --with-nth=1,2 | awk -F'\\0' '{{print $3}}'
        """
    ),
    dc_run_global=dict(
        description='Run commands and aliases (global)',
        command="""
            eval `dc_search_target_global`
        """
    ),

)
