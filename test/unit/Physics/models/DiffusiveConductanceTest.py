import OpenPNM
import pytest
import scipy as sp


class DiffusiveConductanceTest:
    def setup_class(self):
        self.net = OpenPNM.Network.Cubic(shape=[5, 5, 5], spacing=1.0)
        self.geo = OpenPNM.Geometry.GenericGeometry(network=self.net,
                                                    pores=self.net.Ps,
                                                    throats=self.net.Ts)
        self.geo['pore.diameter'] = 1.0
        self.geo['pore.area'] = 1.0
        self.geo['throat.diameter'] = 1.0
        self.geo['throat.length'] = 1e-9
        self.geo['throat.area'] = 1
        self.air = OpenPNM.Phases.Air(network=self.net)
        self.phys = OpenPNM.Physics.GenericPhysics(network=self.net,
                                                   phase=self.air,
                                                   geometry=self.geo)

    def test_bulk_diffusion(self):
        mod = OpenPNM.Physics.models.diffusive_conductance.bulk_diffusion
        self.phys.models.add(propname='throat.conductance1',
                             model=mod)
        assert sp.allclose(a=self.phys['throat.conductance1'][0],
                           b=0.00084552)

        self.phys.models.add(propname='throat.conductance2',
                             model=mod,
                             calc_pore_len=True)
        assert sp.allclose(a=self.phys['throat.conductance2'][0],
                           b=0.00084552)
