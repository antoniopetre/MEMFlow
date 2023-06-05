from hist import Hist
import hist
import awkward as ak
import numpy as np
import os
import mplhep
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib as mpl

class SavePlots:
    
    def __init__(self, nameDir):
        
        self.nameDir = nameDir
        if os.path.exists(self.nameDir):
            raise Exception("Directory already exists! Use another path")
        else:
            os.mkdir(self.nameDir)
                
                
    def plot_var2d(self, higgs_var1, higgs_var2, thad_var1, thad_var2, tlep_var1, tlep_var2,
             ISR_var1, ISR_var2, name1, name2, nameFig, start1=0, stop1=1000, start2=0, stop2=1000, bins1=100, bins2=100,
             higgs_mask=1, thad_mask=1, tlep_mask=1, ISR_mask=1, neg_Mask=False, log=False):
        
        
        if neg_Mask:
            higgs_mask = np.logical_not(higgs_mask)
            thad_mask = np.logical_not(thad_mask)
            tlep_mask = np.logical_not(tlep_mask)
            ISR_mask = np.logical_not(ISR_mask)

        # Quick construction, no other imports needed:
        hist2d_var_higgs = (
          Hist.new
          .Reg(bins=bins1, start=start1, stop=stop1, name=name1, label=name1)
          .Reg(bins=bins2, start=start2, stop=stop2, name=name2, label=name2)
          .Double())

        hist2d_var_thad = (
          Hist.new
          .Reg(bins=bins1, start=start1, stop=stop1, name=name1, label=name1)
          .Reg(bins=bins2, start=start2, stop=stop2, name=name2, label=name2)
          .Double())

        hist2d_var_tlep = (
          Hist.new
          .Reg(bins=bins1, start=start1, stop=stop1, name=name1, label=name1)
          .Reg(bins=bins2, start=start2, stop=stop2, name=name2, label=name2)
          .Double())

        hist2d_var_ISR = (
          Hist.new
          .Reg(bins=bins1, start=start1, stop=stop1, name=name1, label=name1)
          .Reg(bins=bins2, start=start2, stop=stop2, name=name2, label=name2)
          .Double())

        hist2d_var_higgs.fill(higgs_var1[higgs_mask],
                            higgs_var2[higgs_mask])

        hist2d_var_thad.fill(thad_var1[thad_mask],
                            thad_var2[thad_mask])

        hist2d_var_tlep.fill(tlep_var1[tlep_mask],
                            tlep_var2[tlep_mask])

        hist2d_var_ISR.fill(ISR_var1[ISR_mask],
                            ISR_var2[ISR_mask])

        fig, axs = plt.subplots(1, 4, figsize=(16, 8))

        if log:
            mplhep.hist2dplot(hist2d_var_higgs, cmap="cividis", norm=mpl.colors.LogNorm(vmin=1), ax=axs[0])

            mplhep.hist2dplot(hist2d_var_thad, cmap="cividis", norm=mpl.colors.LogNorm(vmin=1), ax=axs[1])

            mplhep.hist2dplot(hist2d_var_tlep, cmap="cividis", norm=mpl.colors.LogNorm(vmin=1), ax=axs[2])

            mplhep.hist2dplot(hist2d_var_ISR, cmap="cividis", norm=mpl.colors.LogNorm(vmin=1), ax=axs[3])

        else:
            mplhep.hist2dplot(hist2d_var_higgs, cmap="cividis", cmin=1, ax=axs[0])

            mplhep.hist2dplot(hist2d_var_thad, cmap="cividis", cmin=1, ax=axs[1])

            mplhep.hist2dplot(hist2d_var_tlep, cmap="cividis", cmin=1, ax=axs[2])

            mplhep.hist2dplot(hist2d_var_ISR, cmap="cividis", cmin=1, ax=axs[3])

        plt.tight_layout()
        plt.savefig(self.nameDir + '/' + nameFig)

    def plot_var1d(self, higgs_var1, thad_var1, tlep_var1, ISR_var1, name1, nameFig, start1=0, stop1=1000, bins1=100,
             higgs_mask=1, thad_mask=1, tlep_mask=1, ISR_mask=1, neg_Mask=False, log=False):
        
        if neg_Mask:
            higgs_mask = np.logical_not(higgs_mask)
            thad_mask = np.logical_not(thad_mask)
            tlep_mask = np.logical_not(tlep_mask)
            ISR_mask = np.logical_not(ISR_mask)

        # Quick construction, no other imports needed:
        hist1d_var_higgs = Hist(hist.axis.Regular(bins=bins1, start=start1, stop=stop1, name=name1))
        
        hist1d_var_thad = Hist(hist.axis.Regular(bins=bins1, start=start1, stop=stop1, name=name1))

        hist1d_var_tlep = Hist(hist.axis.Regular(bins=bins1, start=start1, stop=stop1, name=name1))

        hist1d_var_ISR = Hist(hist.axis.Regular(bins=bins1, start=start1, stop=stop1, name=name1))


        hist1d_var_higgs.fill(higgs_var1[higgs_mask])

        hist1d_var_thad.fill(thad_var1[thad_mask])

        hist1d_var_tlep.fill(tlep_var1[tlep_mask])

        hist1d_var_ISR.fill(ISR_var1[ISR_mask])

        fig, axs = plt.subplots(1, 4, figsize=(16, 8))

        if log:
            mplhep.histplot(hist1d_var_higgs, ax=axs[0])

            mplhep.histplot(hist1d_var_thad, ax=axs[1])

            mplhep.histplot(hist1d_var_tlep, ax=axs[2])

            mplhep.histplot(hist1d_var_ISR, ax=axs[3])

        else:
            mplhep.histplot(hist1d_var_higgs, ax=axs[0])

            mplhep.histplot(hist1d_var_thad, ax=axs[1])

            mplhep.histplot(hist1d_var_tlep, ax=axs[2])

            mplhep.histplot(hist1d_var_ISR, ax=axs[3])

        plt.tight_layout()
        plt.savefig(self.nameDir + '/' + nameFig)
        
    def plot_particle(self, particleCorrect, particle, nameFig, particle_mask=1, neg_Mask=False, log=False):
        
        if neg_Mask:
            particle_mask = np.logical_not(particle_mask)

        hist2d_E_thad = (
          Hist.new
          .Reg(bins=150, start=100, stop=2000, name="E-correct", label="E-correct")
          .Reg(bins=150, start=100, stop=2000, name="E-regressed", label="E-regressed")
          .Double())

        hist2d_px_thad = (
          Hist.new
          .Reg(bins=100, start=-1500, stop=1500, name="px-correct", label="px-correct")
          .Reg(bins=100, start=-1500, stop=1500, name="px-regressed", label="px-regressed")
          .Double())

        hist2d_py_thad = (
          Hist.new
          .Reg(bins=100, start=-1500, stop=1500, name="py-correct", label="py-correct")
          .Reg(bins=100, start=-1500, stop=1500, name="py-regressed", label="py-regressed")
          .Double())

        hist2d_pz_thad = (
          Hist.new
          .Reg(bins=100, start=-2500, stop=2500, name="pz-correct", label="pz-correct")
          .Reg(bins=100, start=-2500, stop=2500, name="pz-regressed", label="pz-regressed")
          .Double())

        hist2d_E_thad.fill(particleCorrect.E[particle_mask],
                        particle.E[particle_mask])

        hist2d_px_thad.fill(particleCorrect.px[particle_mask],
                        particle.px[particle_mask])

        hist2d_py_thad.fill(particleCorrect.py[particle_mask],
                        particle.py[particle_mask])

        hist2d_pz_thad.fill(particleCorrect.pz[particle_mask],
                        particle.pz[particle_mask])

        fig, axs = plt.subplots(2, 2, figsize=(16, 8))

        if log:

            mplhep.hist2dplot(hist2d_E_thad, cmap="cividis", norm=mpl.colors.LogNorm(vmin=1), ax=axs[0, 0])

            mplhep.hist2dplot(hist2d_px_thad, cmap="cividis", norm=mpl.colors.LogNorm(vmin=1), ax=axs[0, 1])

            mplhep.hist2dplot(hist2d_py_thad, cmap="cividis", norm=mpl.colors.LogNorm(vmin=1), ax=axs[1, 0])

            mplhep.hist2dplot(hist2d_pz_thad, cmap="cividis", norm=mpl.colors.LogNorm(vmin=1), ax=axs[1, 1])

        else:
            mplhep.hist2dplot(hist2d_E_thad, cmap="cividis", cmin=1, ax=axs[0, 0])

            mplhep.hist2dplot(hist2d_px_thad, cmap="cividis", cmin=1, ax=axs[0, 1])

            mplhep.hist2dplot(hist2d_py_thad, cmap="cividis", cmin=1, ax=axs[1, 0])

            mplhep.hist2dplot(hist2d_pz_thad, cmap="cividis", cmin=1, ax=axs[1, 1])

        plt.tight_layout()
        plt.savefig(self.nameDir + '/' + nameFig)
        
        
    def plot_rambo(self, rambo_correct, rambo_regressed, nameFig, typePlot=0, log=False):
        if (typePlot > 2):
            typePlot = 2

        hist2d_rambo_0 = (
          Hist.new
          .Reg(bins=200, start=-0.05, stop=1, name=f"rambo-correct-{4*typePlot}", label=f"rambo-correct-{4*typePlot}")
          .Reg(bins=200, start=-0.05, stop=1, name=f"rambo-regressed-{4*typePlot}", label=f"rambo-regressed-{4*typePlot}")
          .Double())

        hist2d_rambo_1 = (
          Hist.new
          .Reg(bins=200, start=-0.05, stop=1, name=f"rambo-correct-{4*typePlot + 1}", label=f"rambo-correct-{4*typePlot + 1}")
          .Reg(bins=200, start=-0.05, stop=1, name=f"rambo-regressed-{4*typePlot + 1}", label=f"rambo-regressed-{4*typePlot + 1}")
          .Double())

        hist2d_rambo_0.fill(rambo_correct[:,4*typePlot],
                        rambo_regressed[:,4*typePlot])

        hist2d_rambo_1.fill(rambo_correct[:,4*typePlot + 1],
                        rambo_regressed[:,4*typePlot + 1])

        num_plots = 2
    
        if typePlot < 2:
            hist2d_rambo_2 = (
              Hist.new
              .Reg(bins=200, start=-0.05, stop=1, name=f"rambo-correct-{4*typePlot + 2}", label=f"rambo-correct-{4*typePlot + 2}")
              .Reg(bins=200, start=-0.05, stop=1, name=f"rambo-regressed-{4*typePlot + 2}", label=f"rambo-regressed-{4*typePlot + 2}")
              .Double())

            hist2d_rambo_3 = (
              Hist.new
              .Reg(bins=200, start=-0.05, stop=1, name=f"rambo-correct-{4*typePlot + 3}", label=f"rambo-correct-{4*typePlot + 3}")
              .Reg(bins=200, start=-0.05, stop=1, name=f"rambo-regressed-{4*typePlot + 3}", label=f"rambo-regressed-{4*typePlot + 3}")
              .Double())

            hist2d_rambo_2.fill(rambo_correct[:,4*typePlot + 2],
                        rambo_regressed[:,4*typePlot + 2])

            hist2d_rambo_3.fill(rambo_correct[:,4*typePlot + 3],
                            rambo_regressed[:,4*typePlot + 3])

            num_plots = 4


        fig, axs = plt.subplots(1, num_plots, figsize=(16, 8))
    
        if log:
            mplhep.hist2dplot(hist2d_rambo_0, cmap="cividis", norm=mpl.colors.LogNorm(vmin=1), ax=axs[0])
            mplhep.hist2dplot(hist2d_rambo_1, cmap="cividis", norm=mpl.colors.LogNorm(vmin=1), ax=axs[1])

            if typePlot < 2:
                mplhep.hist2dplot(hist2d_rambo_2, cmap="cividis", norm=mpl.colors.LogNorm(vmin=1), ax=axs[2])
                mplhep.hist2dplot(hist2d_rambo_3, cmap="cividis", norm=mpl.colors.LogNorm(vmin=1), ax=axs[3])

        else:
            mplhep.hist2dplot(hist2d_rambo_0, cmap="cividis", cmin=1, ax=axs[0])
            mplhep.hist2dplot(hist2d_rambo_1, cmap="cividis", cmin=1, ax=axs[1])

            if typePlot < 2:
                mplhep.hist2dplot(hist2d_rambo_2, cmap="cividis", cmin=1, ax=axs[2])
                mplhep.hist2dplot(hist2d_rambo_3, cmap="cividis", cmin=1, ax=axs[3])

        plt.tight_layout()
        plt.savefig(self.nameDir + '/' + nameFig)
      
    
    
class FindMasks:

    def higgs_mask(self, jets):
        prov1_jets = jets[jets.prov == 1]
        prov1 = prov1_jets["prov"]
        higgs_mask = ak.count(prov1, axis=1) == 2
        
        higgs_mask = ak.to_numpy(higgs_mask)
        return higgs_mask
    
    def thad_mask(self, jets):
        prov2_jets = jets[jets.prov == 2] # b from hadronic top decay
        prov2 = prov2_jets["prov"]
        hadb_mask = ak.count(prov2, axis=1) == 1
        
        prov5_jets = jets[jets.prov == 5] # q from hadronic W decay
        prov5 = prov5_jets["prov"]
        hadW_mask = ak.count(prov5, axis=1) == 2
        
        hadb_mask = ak.to_numpy(hadb_mask)
        hadW_mask = ak.to_numpy(hadW_mask)
        
        thad_mask = np.logical_and(hadb_mask, hadW_mask)
        return thad_mask
    
    def tlep_mask(self, jets):
        prov3_jets = jets[jets.prov == 3] # b from lept top decay
        prov3 = prov3_jets["prov"]
        
        blep_mask = ak.count(prov3, axis=1) == 1
        tlep_mask = ak.to_numpy(blep_mask)
        
        return tlep_mask
    
    def ISR_mask(self, jets):
        prov4_jets = jets[jets.prov == 4]
        prov4 = prov4_jets["prov"]
        
        ISR_mask = ak.count(prov4, axis=1) == 1
        ISR_mask = ak.to_numpy(ISR_mask)
        
        return ISR_mask
        
        
        
        