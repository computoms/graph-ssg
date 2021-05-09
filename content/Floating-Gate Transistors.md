{
	"Abstract": "", 
	"Parents": ["Flash Drives", "SSD"], 
	"Children": ["Electric Force"], 
	"Title": "Floating-Gate Transistors", 
	"Date": "2020-07-20"
}

# Floating-Gate Transistors

The electronic component that forms the basis of a flash memory is called a *Floating gate transistor* (FG Transistor). It is a MOSFET transistor with the MOS structure -- that contains the gate of the transistor -- modified. Instead of having the three-layer structure metal-oxide-semiconductor; we have a five-layer structure: metal-oxide-metal-oxide-semiconductor (MOMOS). The structure is represented in the following image.

<img src="images/articles/FGTransistor.png" class="w3-center" width="60%" />

The middle part is composed of a metallic gate, that is stacked over an insulator (usually, an oxide such as silicon oxide) on top of a second metallic part -- called the floating-gate -- on top of another insulator layer of a slightly different thickness which in turn is placed over the semiconductor substrate that form the backbone of the transistor.


## Principle of operation

The FG transistor works a bit like a capacitor: its floating gate part can be electrically charged or discharged. Basically, when the floating gate of the transistor is charged, the transistor is passing -- it lets the current flow from its source to drain terminals. When the floating gate is not charged, it is blocking. This way, we can encode bit 1 (FG charged) or 0 (FG discharged). 

But, if the principle is similar to the capacitor, why do capacitors inside DRAMs loose their charge after a while and need a refresh mechanism whereas FG transistors do not?

The answer lies in the physical principle that is at play in a floating-gate transistor.

## Physical principle

The FG transistor is different from a capacitor: the electrons that are stored in the floating gate are forced into this area using a different physical principle than when charging a capacitor. 

When charging a capacitor, you typically apply a voltage between its terminals in order to move electrons from one plate to the other. Electrons are flowing through metallic plates and metallic wires -- conductive materials. 

To charge the floating-gate of a FG transistor, you apply a large voltage on its *gate* terminal while also applying a voltage on its source terminal. While a large voltage on the gate of the transistor opens its channel so that electrons can flow from source to drain, it also produces an electric field inside the MOMOS structure so that electrons are attracted to the gate terminal. Because of the oxide layers -- that are electrically insulating materials -- electrons cannot flow from source to gate. But if the voltage is large enough, and the oxide layer is thin enough, a physical phenomenon can occur that allows electrons to *jump* from the semiconductor to the metal of the floating-gate -- passing through the oxide layer. This phenomenon is called **quantum tunnelling**. 

When some electrons were able to jump from the semiconductor into the floating-gate, and we remove the voltages, they have no more the possibility to jump back to the semiconductor, because no more "large" voltage is applied. They stay here forever. That is what makes the Flash memories persistent. 