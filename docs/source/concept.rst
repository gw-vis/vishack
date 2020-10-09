Concept
=======

What is VISHack?
----------------
VISHack stands for Vibration Isolation System Health Check.

Here vibration islation systems are referred to suspensions in KAGRA used
to suspend optics of the gravitational wave detector.

What is "health check"?
-----------------------
Health checks tell if a suspension behaves normally. Checks are usually
required after traumatic events such as earthquakes. In conventional system
health checks, the expert typically uses diaggui measurement templates with
reference plots of transfer functions to do the measurement.
The new measurements are then compared to the references visually. Then
the expert decides, according to the judgement, whether or not the system
is healthy.

Why VISHack?
------------
While the traditional method works fine, VISHack provides a more systematic
way to perform consistent system health checks conveniently. Since it is
powered by Python, it would be possible to automate system health checks,
for example, with Guardian, which is a state-machine software used in KAGRA
inherited from LIGO. Nevertheless, VISHack is designed to be extremely
easy to use. So, anyone can perform system-diagnosis on vibration isolation
systems, say, with a click of a button or a line of command.

How does VISHack work?
----------------------
VISHack takes a :ref:`Configuration File`, which has specified paths, among
other settings, of certain diaggui XML files that are dedicated for system
health checks.
In the diaggui files, there should be some references of the same measurement
that defines the "healthy" state of that particular measurement. VISHack
can trigger measurements using the diaggui file, and reads new recordings
using the :code:`dtt2hdf` package. VISHack will then compare the measurement
results with the references. If the new measurements are very different from
the healthy references, then users will be alerted.

How does VISHack identify unhealthy systems?
--------------------------------------------
VISHack evaluates certain statistical quantities :math:`Q`
using/comparing the new measurement and the healthy references.
As of v1.0.0, available
options of these quantities are mean squared error (MSE) and maximum absolute
error (MAE) between the result and the references,
and root mean square (RMS) of the measurement data.
There are options to weight/whiten
the data with the inverse of the reference before evaluating. These quantities
are prefixed with the letter W, i.e. WMSE, WMAE, and WRMS.

The quantities of a particular measurement result are evaluated for each
available references and hence the average :math:`\left\langle Q\right\rangle`
is obtained. Then, the same evaluation is done using each reference as the
measurement and the rest of the available references as the healthy references.
Hence, using only the references, the expected value of of the quantity
:math:`\left\langle Q_\mathrm{ref}\right\rangle` and the standard deviation
:math:`\sigma_{Q_\mathrm{ref}}` are obtained.

Finally, the two :math:`Q` s are compared and presented in units the standard
deviation :math:`\sigma_{Q_\mathrm{ref}}`, i.e.

.. math::

   \left\langle Q\right\rangle-\left\langle Q_\mathrm{ref}\right\rangle
   =d\,\sigma_{Q_\mathrm{ref}},

where :math:`d` is a constant representing the difference between the
current measurement and the health references. When
:math:`\left\lvert d\right\rvert` is larger than a defined threshold, then
the system is considered unhealthy and would require further attention from
experts.
