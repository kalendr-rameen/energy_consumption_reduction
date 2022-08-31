# energy_consumption_reduction


In order to optimize production costs, the steelworks of So Hardening Steel Ltd. decided to reduce electricity consumption during the steel processing phase. You will have to build a model that predicts the temperature of the steel.

### Description of the processing step.

Steel is processed in a metal ladle with a capacity of about 100 tons. In order for the ladle to withstand the high temperatures, it is lined with refractory bricks from the inside. Molten steel is poured into the ladle and heated to the desired temperature by graphite electrodes. These are installed in the ladle lid. 

Sulfur is removed from the alloy (desulfurization), the chemical composition is corrected by adding impurities and samples are taken. The steel is alloyed - its composition is changed - by feeding pieces of alloy from the bulk material bin or wire through a special tribe (tribe, "mass").

Before the alloying additives are introduced for the first time, the temperature of the steel is measured and a chemical analysis is made. Then the temperature is raised for a few minutes, the alloying materials are added and the alloy is purged with inert gas. It is then stirred and measured again. This cycle is repeated until the target chemical composition and optimum melting temperature are achieved.

Then the molten steel is sent for metal finishing or to the continuous casting machine. From there, the finished product comes out in the form of slab billets (*slab*, "slab").


```

Description of the data

The data consists of files obtained from different sources:

- `data_arc.csv` - electrode data;
- `data_bulk.csv` - bulk feed data (volume);
- `data_bulk_time.csv` *-* bulk feed data (time);
- `data_gas.csv` - data on gas purging of the alloy;
- `data_temp.csv` - temperature measurement results;
- `data_wire.csv` - data on wire materials (volume);
- `data_wire_time.csv` - data on wire materials (time).


```


