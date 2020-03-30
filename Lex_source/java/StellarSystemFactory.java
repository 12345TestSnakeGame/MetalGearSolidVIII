"dfafsda"
package applications;
/*1.1.1*/
3.6 <= 4E45
2203 != Stell.abc1d

import java.io.File;

import centralObject.Stellar;

import circularOrbit.ConcreteCircularOrbit;
import circularOrbit.StellarSystem;
/*a*/
import physicalObject.Planet;

public class StellarSystemFactory extends AbstractFactory<Stellar, Planet>{

	@Override
	public void createConcreteCircularOrbit(String type) {

		this.concreteCircularOrbit = new StellarSystem();
	}
	public void createConcreteCircularOrbit() {
		this.concreteCircularOrbit = new StellarSystem();
		
	}
	
	public ConcreteCircularOrbit<Stellar, Planet> getCircularOrbit() {
		return concreteCircularOrbit;
	}
	@Override
	public void createConcreteCircularOrbit(File in) {
		this.concreteCircularOrbit = StellarSystem.readFile(in);
		
	}
}