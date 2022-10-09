import numpy as np

def visualize_data(sim, ax, data, normalized:bool=True, labels:bool=True, title:bool=False, plot_fit:bool=True):
        max_dmg = int(np.max(data)+1)
        bins = np.arange(-0.5*sim.bin_size(), max_dmg, sim.bin_size())
        
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
    return A/np.sqrt(2*np.pi*sigma*sigma)*np.exp(- np.power(x-mu, 2)/(2*sigma*sigma))

def analyze_data_simple(sim, data, normalized:bool = True):
    if normalized:
        return (np.mean(data) , np.std(data))
    else:
        return (np.mean(data) , np.std(data), sim.num_runs)