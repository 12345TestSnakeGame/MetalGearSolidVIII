package applications;

import java.io.File;

import centralObject.Person;
import circularOrbit.ConcreteCircularOrbit;
import circularOrbit.SocialNetworkCircle;

public class SocialNetworkCircleFactory extends AbstractFactory<Person, Person>{

	@Override
	public void createConcreteCircularOrbit(String type) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void createConcreteCircularOrbit(File in) {
		try {
			this.concreteCircularOrbit = SocialNetworkCircle.readFile(in);
		} catch (Exception e) {
			e.printStackTrace();
		}	
	}
	
	public ConcreteCircularOrbit<Person, Person> getCircularOrbit(){
		return this.concreteCircularOrbit;
	}

}
