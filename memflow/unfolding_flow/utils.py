import torch
import vector
import numpy as np
import awkward as ak
from memflow.phasespace.phasespace import PhaseSpace
import memflow.phasespace.utils as utils

M_HIGGS = 125.25
M_TOP = 172.5
M_GLUON = 0.0

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def to_flat_tensor(X, fields, axis=1, allow_missing=False):
    return torch.tensor(np.stack([ak.to_numpy(getattr(X,f), allow_missing=allow_missing) for f in fields], axis=axis))

class Compute_ParticlesTensor:

    def get_HttISR(cond_X, log_mean, log_std, device):

        higgs = cond_X[0].unsqueeze(dim=1)
        thad = cond_X[1].unsqueeze(dim=1)
        tlep = cond_X[2].unsqueeze(dim=1)
        Htt = torch.cat((higgs, thad, tlep), dim=1)

        unscaledlog = Htt*log_std + log_mean
        data_regressed = unscaledlog
        data_regressed[:,:,0] = torch.sign(unscaledlog[:,:,0])*(torch.exp(torch.abs(unscaledlog[:,:,0])) - 1)

        higgs = data_regressed[:,0]
        thad = data_regressed[:,1]
        tlep = data_regressed[:,2]

        higgs = vector.array(
            {
                "pt": higgs[:,0].detach().cpu().numpy(),
                "eta": higgs[:,1].detach().cpu().numpy(),
                "phi": higgs[:,2].detach().cpu().numpy(),
                "mass": M_HIGGS*np.ones(higgs.shape[0])
            }
        )

        thad = vector.array(
            {
                "pt": thad[:,0].detach().cpu().numpy(),
                "eta": thad[:,1].detach().cpu().numpy(),
                "phi": thad[:,2].detach().cpu().numpy(),
                "mass": M_TOP*np.ones(thad.shape[0])
            }
        )

        tlep = vector.array(
            {
                "pt": tlep[:,0].detach().cpu().numpy(),
                "eta": tlep[:,1].detach().cpu().numpy(),
                "phi": tlep[:,2].detach().cpu().numpy(),
                "mass": M_TOP*np.ones(tlep.shape[0])
            }
        )

        higgs = ak.with_name(higgs, name="Momentum4D")
        thad = ak.with_name(thad, name="Momentum4D")
        tlep = ak.with_name(tlep, name="Momentum4D")

        gluon_px = -(higgs.px + thad.px + tlep.px)
        gluon_py = -(higgs.py + thad.py + tlep.py)
        gluon_pz = -(higgs.pz + thad.pz + tlep.pz)
        E_gluon = np.sqrt(gluon_px**2 + gluon_py**2 + gluon_pz**2)

        gluon_px = np.expand_dims(gluon_px, axis=1)
        gluon_py = np.expand_dims(gluon_py, axis=1)
        gluon_pz = np.expand_dims(gluon_pz, axis=1)
        E_gluon = np.expand_dims(E_gluon, axis=1)

        gluon = np.concatenate((E_gluon, gluon_px, gluon_py, gluon_pz), axis=1)

        glISR = vector.array(
            {
                "E": gluon[:,0],
                "px": gluon[:,1],
                "py": gluon[:,2],
                "pz": gluon[:,3],
            }
        )

        glISR = ak.with_name(glISR, name="Momentum4D")

        higgs_tensor = to_flat_tensor(higgs, ["t", "x", "y", "z"], axis=1, allow_missing=False).unsqueeze(dim=1)
        thad_tensor = to_flat_tensor(thad, ["t", "x", "y", "z"], axis=1, allow_missing=False).unsqueeze(dim=1)
        tlep_tensor = to_flat_tensor(tlep, ["t", "x", "y", "z"], axis=1, allow_missing=False).unsqueeze(dim=1)
        gluon_tensor = torch.Tensor(gluon).unsqueeze(dim=1)

        data_regressed = torch.cat((higgs_tensor, thad_tensor, tlep_tensor, gluon_tensor), dim=1)

        boost_regressed = higgs + thad + tlep + glISR
        boost_regressed = to_flat_tensor(boost_regressed, ["t", "x", "y", "z"], axis=1, allow_missing=False)

        if (device == torch.device('cuda')):
            data_regressed = data_regressed.cuda()
            boost_regressed = boost_regressed.cuda()
        
        return data_regressed, boost_regressed

    def get_cartesian_comp(particle, mass):

        particle_cartesian = torch.zeros((particle.shape[0], 4))
        
        # px
        particle_cartesian[:,1] = particle[:,0]*torch.cos(particle[:,2])

        # py
        particle_cartesian[:,2] = particle[:,0]*torch.sin(particle[:,2])

        # pz
        particle_cartesian[:,3] = particle[:,0]*torch.sinh(particle[:,1])

        particle2 = particle_cartesian.clone()

        # E
        particle_cartesian[:,0] = torch.sqrt(particle2[:,1]**2 + particle2[:,2]**2 + particle2[:,3]**2 + mass**2)

        return particle_cartesian

    def get_HttISR_numpy(cond_X, log_mean, log_std, device, eps=0.0):

        higgs = cond_X[0].unsqueeze(dim=1)
        thad = cond_X[1].unsqueeze(dim=1)
        tlep = cond_X[2].unsqueeze(dim=1)
        Htt = torch.cat((higgs, thad, tlep), dim=1)

        unscaledlog = Htt*log_std + log_mean
        data_regressed = unscaledlog.clone()
        data_regressed[:,:,0] = torch.sign(unscaledlog[:,:,0])*(torch.exp(torch.abs(unscaledlog[:,:,0])) - 1)

        higgs = data_regressed[:,0]
        thad = data_regressed[:,1]
        tlep = data_regressed[:,2]

        higgs_cartesian = Compute_ParticlesTensor.get_cartesian_comp(higgs, M_HIGGS).unsqueeze(dim=1)
        thad_cartesian = Compute_ParticlesTensor.get_cartesian_comp(thad, M_TOP).unsqueeze(dim=1)
        tlep_cartesian = Compute_ParticlesTensor.get_cartesian_comp(tlep, M_TOP).unsqueeze(dim=1)

        gluon_px = -(higgs_cartesian[:,0,1] + thad_cartesian[:,0,1] + tlep_cartesian[:,0,1]).unsqueeze(dim=1)
        gluon_py = -(higgs_cartesian[:,0,2] + thad_cartesian[:,0,2] + tlep_cartesian[:,0,2]).unsqueeze(dim=1)
        gluon_pz = -(higgs_cartesian[:,0,3] + thad_cartesian[:,0,3] + tlep_cartesian[:,0,3]).unsqueeze(dim=1)
        E_gluon = torch.sqrt(gluon_px**2 + gluon_py**2 + gluon_pz**2) + eps # add epsilon to have positive masses of the gluon
        gluon_cartesian = torch.cat((E_gluon, gluon_px, gluon_py, gluon_pz), dim=1).unsqueeze(dim=1)

        data_regressed = torch.cat((higgs_cartesian, thad_cartesian, tlep_cartesian, gluon_cartesian), dim=1)
        # order: by default higgs/thad/tlep/glISR
        # but for glISR negative masses in Rambo ==> can switch the order of the data_regressed
        # I changed to do this permutation of the particles inside the get_PS

        boost_regressed = gluon_cartesian + higgs_cartesian + thad_cartesian + tlep_cartesian
        boost_regressed = boost_regressed.squeeze(dim=1)

        if (device == torch.device('cuda')):
            data_regressed = data_regressed.cuda()
            boost_regressed = boost_regressed.cuda()
        
        return data_regressed, boost_regressed

    def get_PS(data_HttISR, boost_reco, order=[0,1,2,3], target_mass=torch.Tensor([[M_HIGGS, M_TOP, M_TOP, M_GLUON]])):

        # do the permutation of H t t ISR
        perm = torch.LongTensor(order)
        data_HttISR = data_HttISR[:,perm,:]

        E_CM = 13000

        boost_reco = boost_reco.squeeze(dim=1)
        # check order of components of boost_reco
        x1 = (boost_reco[:, 0] + boost_reco[:, 3]) / E_CM
        x2 = (boost_reco[:, 0] - boost_reco[:, 3]) / E_CM

        mask1 = x1 < 0
        mask2 = x2 < 0
        if (mask1.any() or mask2.any()):
            print("ERROR: x1 or x2 lower than 0")
            exit(0)

        n = 4
        nDimPhaseSpace = 8

        masses_t = target_mass[:,perm]
        #print(masses_t.shape)

        P = data_HttISR.clone()  # copy the final state particless
        
        # Check if we are in the CM
        ref_lab = torch.sum(P, axis=1)
        if not ((utils.rho2_t(ref_lab) < 1e-3).any()):
            raise Exception("Momenta batch not in the CM, failing to convert back to PS point")
        
        # We start getting M and then K
        M = torch.tensor(
            [0.0] * n, requires_grad=False, dtype=torch.double, device=P.device
        )
        M = torch.unsqueeze(M, 0).repeat(P.shape[0], 1)
        K_t = M.clone()
        Q = torch.zeros_like(P).to(P.device)
        Q[:, -1] = P[:, -1]  # Qn = pn

        # intermediate mass
        for i in range(n, 0, -1):
            j = i - 1
            square_t_P = utils.square_t(torch.sum(P[:, j:n], axis=1))
            M[:, j] = torch.sqrt(square_t_P)

            # new version
            #M[:, j] = torch.nan_to_num(M[:, j], nan=0.0)

            # Remove the final masses to convert back to K
            K_t[:, j] = M[:,j] - torch.sum(masses_t[:,j:])

        # output [0,1] distributed numbers        
        r = torch.zeros(P.shape[0], nDimPhaseSpace, device=P.device)

        for i in range(n, 1, -1):
            j = i - 1  # index for 0-based tensors
            # in the direct algo the u are squared.

            u = (K_t[:, j]/K_t[:, j-1]) ** 2

            r[:, j - 1] = (n + 1 - i) * (torch.pow(u, (n - i))) - (n - i) * (
                torch.pow(u, (n + 1 - i))
            )

            Q[:, j - 1] = Q[:, j] + P[:, j - 1]

            P[:, j - 1] = utils.boost_t(P[:, j - 1], -1*utils.boostVector_t(Q[:, j - 1]))

            P_copy = P.clone().to(P.device)
            r[:, n - 5 + 2 * i - 1] = (
                (P_copy[:, j - 1, 3] / torch.sqrt(utils.rho2_t(P_copy[:, j - 1]))) + 1
            ) / 2
            # phi= tan^-1(Py/Px)
            phi = torch.atan(P_copy[:, j - 1, 2] / P_copy[:, j - 1, 1])
            # Fixing phi depending on X and y sign
            # 4th quandrant  (px > 0, py < 0)
            deltaphi = torch.where(
                (P_copy[:, j - 1, 2] < 0) & (P_copy[:, j - 1, 1] > 0), 2 * torch.pi, 0.0
            )
            # 2th and 3th quadratant  (px < 0, py whatever)
            deltaphi += torch.where((P_copy[:, j - 1, 1] < 0), torch.pi, 0.0)
            phi += deltaphi
            r[:, n - 4 + 2 * i - 1] = phi / (2 * torch.pi)

        detjinv_regressed = 0

        maskr_0 = r < 0
        maskr_1 = r > 1
        
        if (maskr_0.any() or maskr_1.any()):
            print("ERROR: r lower than 0")
            print(r[maskr_0])
            print(r[maskr_1])
            exit(0)

        x1 = x1.unsqueeze(dim=1)
        x2 = x2.unsqueeze(dim=1)
        return torch.cat((r, x1, x2), axis=1), detjinv_regressed
