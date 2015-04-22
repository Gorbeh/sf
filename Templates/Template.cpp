/*
**-----------------------------------------------------------------------------
**  Created by sfunctioner v1.0.0
**	https://sourceforge.net/projects/sfunctioner/
**-----------------------------------------------------------------------------
*/

/* Give S-function a name */
#define S_FUNCTION_NAME  $SFUNCTION_NAME$
#define S_FUNCTION_LEVEL 2

/* Include SimStruct definition and file I/O functions */
#include "simstruc.h"
#include "$SFUNCTION_NAME$.h"

#ifdef __cplusplus
extern "C" { // use the C fcn-call standard for all functions
#endif       // defined within this scope

/* Called at the beginning of the simulation */
static void mdlInitializeSizes(SimStruct *S)
{
	$PARAM_PTR_DEFINE_INIT$

$SET_SIMULATION_OPTIONS$

    ssSetNumSFcnParams(S, SFUNCTION_PARAM_NUM);
    if (ssGetNumSFcnParams(S) != ssGetSFcnParamsCount(S))
        return;

    ssSetNumContStates(S, $SFUNCTION_CONT_STATE_NUM$);
    ssSetNumDiscStates(S, $SFUNCTION_DISC_STATE_NUM$);

$SET_PORTS$

$PARAMETER_SETUP_INIT$

    ssSetNumSampleTimes(S, 1);

$PARAMETER_DEL_INIT$
}


/* Set sample times for the block */
static void mdlInitializeSampleTimes(SimStruct *S)
{
    ssSetSampleTime(S, 0, $SFUNCTION_SAMPLE_TIME$);
    ssSetOffsetTime(S, 0, $SFUNCTION_OFFSET_TIME$);
}



#define MDL_START
#if defined(MDL_START)
/* Function: mdlStart =======================================================
* Abstract:
*    This function is called once at start of model execution. If you
*    have states that should be initialized once, this is the place
*    to do it.
*/
static void mdlStart(SimStruct *S)
{
	$PARAM_PTR_DEFINE_START$

$PARAMETER_SETUP_START$



$PARAMETER_DEL_START$
}
#endif /*  MDL_START */



/* Function: mdlOutputs =======================================================
 * Abstract:
 *    In this function, you compute the outputs of your S-function
 *    block.
 */
static void mdlOutputs(SimStruct *S, int_T tid)
{
	$PARAM_PTR_DEFINE_OUTPUTS$

$PARAMETER_SETUP_OUTPUTS$

	$SET_PORT_ARRAY_POINTERS$

	$SET_PORT_POINTERS$

$PARAMETER_DEL_OUTPUTS$
}

/* Function: mdlTerminate =====================================================
 * Abstract:
 *    In this function, you should perform any actions that are necessary
 *    at the termination of a simulation.  For example, if memory was
 *    allocated in mdlStart, this is the place to free it.
 */
static void mdlTerminate(SimStruct *S)
{
}


/*=============================*
 * Required S-function trailer *
 *=============================*/

#ifdef  MATLAB_MEX_FILE    /* Is this file being compiled as a MEX-file? */
#include "simulink.c"      /* MEX-file interface mechanism */
#else
#include "cg_sfun.h"       /* Code generation registration function */
#endif

#ifdef __cplusplus
} // end of extern "C" scope
#endif
