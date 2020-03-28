package applications;
 
import java.io.File;

import centralObject.CentralObject;
import circularOrbit.CircularOrbit;
import circularOrbit.ConcreteCircularOrbit;
import physicalObject.PhysicalObject;

public abstract class AbstractFactory<L,E> {
	/*
	 * 
	 */
	protected ConcreteCircularOrbit<L, E> concreteCircularOrbit;
	
	public CircularOrbit<L, E> getCircularOrbit() {
		return concreteCircularOrbit;
	}
	
	public abstract void createConcreteCircularOrbit(String type);
	
	public abstract void createConcreteCircularOrbit(File in);
	
	
}
