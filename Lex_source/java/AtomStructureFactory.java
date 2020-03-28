package applications;

import java.io.File;

import centralObject.AtomCore;
import circularOrbit.AtomStructure;
import circularOrbit.ConcreteCircularOrbit;
import physicalObject.Electron;

public class AtomStructureFactory extends AbstractFactory<AtomCore, Electron> {

	@Override
	public void createConcreteCircularOrbit(String type) {
		// TODO Auto-generated method stub
		
	}
	public void createConcreteCircularOrbit(File in) {
		try {
			this.concreteCircularOrbit = AtomStructure.readFile(in);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	public ConcreteCircularOrbit<AtomCore, Electron> getCircularOrbit(){
		return this.concreteCircularOrbit;
	}
}
