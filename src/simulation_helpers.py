import numpy as np

def visualize_data(sim, ax, data, normalized:bool=True, labels:bool=True, title:bool=False, plot_fit:bool=True):
    '''
        This method visualizes the damage data of a simulation run inside a provided matplotlib Axis object.
        It works in-place and adds the histogram and potentially the gaussian distribution to the axis object.
        
        params:
        - sim: Simulation Object which includes data for attacker, target, weapon and modifiers
        - ax: matplotlib Axis object we plot data to.
        - data: the results of a simulation run of inflicted damage
        - normalized: boolean, should the histogram be plotted normaized or not?
        - labels: boolean, should labels be provided for axis and titles? automatically generated from sim.
        - title: boolean, should a title be generated? automatically generated from sim.
        - plot_fit: boolean, fit gaussian distribtion to data and plot distribution
    '''
    max_dmg = int(np.max(data)+1)
    bins = np.arange(-0.5*bin_size(sim), max_dmg, bin_size(sim))
    
    if(sim.target.unit_type=='infantry'):
        xlabel = f'Number of {sim.target.name} slain'
    else:
        xlabel = f'Damage infliceted to {sim.target.name}'
    if not normalized and labels:
        ylabel = 'Number of events'
    elif labels:
        ylabel = 'Relative probability'
        
    ax.hist(data, bins=bins, density=normalized, label='simulated damage')
    if plot_fit:
        params = analyze_data_simple(sim, data, normalized)
        x = np.linspace(np.min(bins), np.max(bins), 100)
        ax.plot(x, gauss(x, *params), 'r:', label='fitted distribution')
    if labels:
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
    if title:
        ax.set_title(f'{sim.attacker.name} attacking {sim.target.name} with {sim.weapon.name}')
    ax.legend()
        
def gauss(x, mu, sigma, A=1):
    '''
        This methods represents a gaussian distribution with epxectation value mu, standard deviation sigma
        and normalization constant A.
        
        - x: double or numpy array, datapoint(s) where the distribution should be evaluated.
        - mu: expectation value of the distribution
        - sigma: standard deviation of the distribution.
        - A: normalization constant, defaults to 1 for PDF.
        
        returns:
        Value of the gaussian distribution at the given datapoit(s)
    '''
    return A/np.sqrt(2*np.pi*sigma*sigma)*np.exp(- np.power(x-mu, 2)/(2*sigma*sigma))

def analyze_data_simple(sim, data, normalized:bool = True):
    '''
        This method analyzes the data from a simulation run and assumes a gausian distribution of the data.
        
        params:
        - sim: Simulation object, needed for normalization constant.
        - data: data of simulation run of inflicted damage.
        - normalized: boolean, should the distribution be normalized or not
    '''
    if normalized:
        return (np.mean(data) , np.std(data))
    else:
        return (np.mean(data) , np.std(data), sim.num_runs)
    
def bin_size(sim)->float:
    '''
        This method calculates bin size for data analysis and visualization
        depending on the parameters of the simulation.
        
        params:
        - sim: Simulation object to caluclate the bin width for.
    '''
    #differentiate between target unit types
    if(sim.target.unit_type=='vehicle'):
        #differentiate between random and flat damage weapons
        if(sim.weapon.dmg_type=='random' or sim.weapon.dmg_type=='mixed'):
            return float(1 + sim.weapon.dmg_mod + sim.modifiers.dmgmod)
        else:
            return float(sim.weapon.dmg + sim.weapon.dmg_mod+sim.modifiers.dmgmod )
    elif(sim.target.unit_type == 'infantry'):
        if(sim.weapon.dmg_type == 'random' or sim.weapon.dmg_type == 'mixed'):
            min_dmg = 1 + sim.weapon.dmg_mod + sim.modifiers.dmgmod
            if min_dmg >= sim.target.hp :
                return 1.
            else:
                return float(1/sim.target.hp)
        else:
            min_dmg = sim.weapon.dmg + sim.weapon.dmg_mod + sim.modifiers.dmgmod
            if min_dmg >= sim.target.hp:
                return 1.0
            else:
                return float(1/sim.target.hp)
    else:
        return 1.