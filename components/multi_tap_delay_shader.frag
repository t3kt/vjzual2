uniform vec4 tapLengthA;
uniform vec4 tapAlphaA;
uniform vec4 tapLengthB;
uniform vec4 tapAlphaB;
uniform int stepCompMode;
uniform int outputSelect;
uniform int tapCount;
uniform int tapFilter0;
uniform int tapFilter1;
uniform int tapFilter2;
uniform int tapFilter3;
uniform int tapFilter4;
uniform int tapFilter5;
uniform int tapFilter6;
uniform int tapFilter7;

#define COMP_ADD 0
#define COMP_ATOP 1
#define COMP_AVERAGE 2
#define COMP_DIFFERENCE 3
#define COMP_INSIDE 4
#define COMP_MAXIMUM 5
#define COMP_MINIMUM 6
#define COMP_MULTIPLY 7
#define COMP_OUTSIDE 8
#define COMP_OVER 9
#define COMP_SCREEN 10
#define COMP_SUBTRACT 11
#define COMP_UNDER 12

#define FILT_NONE 0
#define FILT_RED 1
#define FILT_GREEN 2
#define FILT_BLUE 3
#define FILT_REDALPHA 4
#define FILT_GREENALPHA 5
#define FILT_BLUEALPHA 6
#define FILT_LUMAALPHA 7

vec4 applyFilter(vec4 color, int mode) {
    if (color.a <= 0.0) {
        return vec4(0.0);
    }
    if (mode <= 0) {
        return color;
    }
    if (mode == FILT_RED) {
        return color * vec4(1.0, 0.0, 0.0, 1.0);
    }
    if (mode == FILT_GREEN) {
        return color * vec4(0.0, 1.0, 0.0, 1.0);
    }
    if (mode == FILT_BLUE) {
        return color * vec4(0.0, 0.0, 1.0, 1.0);
    }
    if (mode <= FILT_BLUEALPHA) {
        color.a = color[mode - FILT_REDALPHA];
        return color;
    }
    if (mode == FILT_LUMAALPHA) {
        color.a = czm_luminance(color.rgb);
        return color;
    }
    return color;
}

#define W_OFFSET uTD3DInfos[0].depth.z

vec4 getTap(float length, float alpha) {
	return texture(sTD3DInputs[0], vec3(vUV.st, length + W_OFFSET)) * vec4(1.0, 1.0, 1.0, alpha);
}

bool[8] getTapStates() {
    bool[8] states;
    #if 0
    states[0] = tapCount >= 1 && tapAlphaA[0] > 0.0;
    states[1] = tapCount >= 2 && tapAlphaA[1] > 0.0;
    states[2] = tapCount >= 3 && tapAlphaA[2] > 0.0;
    states[3] = tapCount >= 4 && tapAlphaA[3] > 0.0;
    states[4] = tapCount >= 5 && tapAlphaB[0] > 0.0;
    states[5] = tapCount >= 6 && tapAlphaB[1] > 0.0;
    states[6] = tapCount >= 7 && tapAlphaB[2] > 0.0;
    states[7] = tapCount >= 8 && tapAlphaB[3] > 0.0;
    #else
    states[0] = tapCount >= 1;
    states[1] = tapCount >= 2;
    states[2] = tapCount >= 3;
    states[3] = tapCount >= 4;
    states[4] = tapCount >= 5;
    states[5] = tapCount >= 6;
    states[6] = tapCount >= 7;
    states[7] = tapCount >= 8;
    #endif

    return states;
}

vec4[8] getTaps(bool[8] states) {
    vec4[8] colors;
    #if 0
    int[4] filtersA = int[4](tapFilter0, tapFilter1, tapFilter2, tapFilter3);
    int[4] filtersB = int[4](tapFilter4, tapFilter5, tapFilter6, tapFilter7);
    for (int i = 0; i < 4; i++) {
        if (tapCount >= i && states[i]) {
            colors[i] = applyFilter(getTap(tapLengthA[i], tapAlphaA[i]), filterA[i]);
        } else {
            colors[i] = vec4(0.0);
        }
    }
    for (int i = 0; i < 4; i++) {
        if (tapCount >= (i + 4) && states[i + 4]) {
            colors[i + 4] = applyFilter(getTap(tapLengthB[i], tapAlphaB[i]), filterB[i]);
        } else {
            colors[i + 4] = vec4(0.0);
        }
    }
    #else
    if (tapCount >= 1 && states[0]) {
        colors[0] = applyFilter(getTap(tapLengthA[0], tapAlphaA[0]), tapFilter0);
    } else {
        colors[0] = vec4(0.0);
    }
    if (tapCount >= 2 && states[1]) {
        colors[1] = applyFilter(getTap(tapLengthA[1], tapAlphaA[1]), tapFilter1);
    } else {
        colors[1] = vec4(0.0);
    }
    if (tapCount >= 3 && states[2]) {
        colors[2] = applyFilter(getTap(tapLengthA[2], tapAlphaA[2]), tapFilter2);
    } else {
        colors[2] = vec4(0.0);
    }
    if (tapCount >= 4 && states[3]) {
        colors[3] = applyFilter(getTap(tapLengthA[3], tapAlphaA[3]), tapFilter3);
    } else {
        colors[3] = vec4(0.0);
    }
    if (tapCount >= 5 && states[4]) {
        colors[4] = applyFilter(getTap(tapLengthB[0], tapAlphaB[0]), tapFilter4);
    } else {
        colors[4] = vec4(0.0);
    }
    if (tapCount >= 6 && states[5]) {
        colors[5] = applyFilter(getTap(tapLengthB[1], tapAlphaB[1]), tapFilter5);
    } else {
        colors[5] = vec4(0.0);
    }
    if (tapCount >= 7 && states[6]) {
        colors[6] = applyFilter(getTap(tapLengthB[2], tapAlphaB[2]), tapFilter6);
    } else {
        colors[6] = vec4(0.0);
    }
    if (tapCount >= 8 && states[7]) {
        colors[7] = applyFilter(getTap(tapLengthB[3], tapAlphaB[3]), tapFilter7);
    } else {
        colors[7] = vec4(0.0);
    }
    #endif
    return colors;
}

vec4 compositeTaps_add(vec4[8] colors, bool[8] states) {
    vec4 color = vec4(0.0);
    for (int i = 0; i < tapCount; i++) {
        if (states[i]) {
            color = color + colors[i];
        }
    }
    return color;
}

vec4 compositeTaps_atop(vec4[8] colors, bool[8] states) {
    vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
    for (int i = 0; i < tapCount; i++) {
        if (states[i]) {
            color = (color.rgba * colors[i].a) + (colors[i].rgba * (1.0 - color.a));
        }
    }
    return color;
}

vec4 compositeTaps_difference(vec4[8] colors, bool[8] states) {
    vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
    for (int i = 0; i < tapCount; i++) {
        if (states[i]) {
            color.rgb = abs(color.rgb - colors[i].rgb);
        }
    }
    return color;
}

vec4 compositeTaps_inside(vec4[8] colors, bool[8] states) {
    vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
    for (int i = 0; i < tapCount; i++) {
        if (states[i]) {
            color = color * clamp(colors[i], 0.0, 1.0);
        }
    }
    return color;
}

vec4 compositeTaps_maximum(vec4[8] colors, bool[8] states) {
    vec4 color = vec4(0.0);
    for (int i = 0; i < tapCount; i++) {
        color = max(color, colors[i]);
    }
    return color;
}

vec4 compositeTaps_minimum(vec4[8] colors, bool[8] states) {
    vec4 color = vec4(1.0);
    for (int i = 0; i < tapCount; i++) {
        if (states[i]) {
            color = min(color, colors[i]);
        }
    }
    return color;
}

vec4 compositeTaps_multiply(vec4[8] colors, bool[8] states) {
    vec4 color = vec4(1.0);
    for (int i = 0; i < tapCount; i++) {
        if (states[i]) {
            color = color * colors[i];
        }
    }
    return color;
}

vec4 compositeTaps_outside(vec4[8] colors, bool[8] states) {
    vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
    for (int i = 0; i < tapCount; i++) {
        if (states[i]) {
            color = color * (1.0 - colors[i].a);
        }
    }
    return color;
}

vec4 compositeTaps_over(vec4[8] colors, bool[8] states) {
    vec4 color = vec4(0.0, 0.0, 0.0, 0.0);
    for (int i = 0; i < tapCount; i++) {
        if (states[i]) {
            color = (colors[i] * (1.0 - color.a)) + color;
        }
    }
    return color;
}

vec4 compositeTaps_screen(vec4[8] colors, bool[8] states) {
    vec4 color = vec4(0.0);
    for (int i = 0; i < tapCount; i++) {
        if (states[i]) {
            color = 1.0 - ((1.0 - color) * (1.0 - colors[i]));
        }
    }
    return color;
}

vec4 compositeTaps_subtract(vec4[8] colors, bool[8] states) {
    vec4 color = vec4(1.0);
    for (int i = 0; i < tapCount; i++) {
        if (states[i]) {
            color = color - colors[i];
        }
    }
    return color;
}

vec4 compositeTaps_under(vec4[8] colors, bool[8] states) {
    vec4 color = vec4(1.0);
    for (int i = 0; i < tapCount; i++) {
        if (states[i]) {
            color = (color * (1.0 - colors[i].a)) + colors[i];
        }
    }
    return color;
}

vec4 compositeTaps(vec4[8] colors, bool[8] states) {
	vec4 color = vec4(0.0);
	if (stepCompMode == COMP_ADD) {
	    return compositeTaps_add(colors, states);
	}
	if (stepCompMode == COMP_ATOP) {
	    return compositeTaps_atop(colors, states);
	}
	if (stepCompMode == COMP_AVERAGE) {
	    return compositeTaps_add(colors, states) / tapCount;
	}
	if (stepCompMode == COMP_DIFFERENCE) {
	    return compositeTaps_difference(colors, states);
	}
	if (stepCompMode == COMP_INSIDE) {
	    return compositeTaps_inside(colors, states);
	}
	if (stepCompMode == COMP_MAXIMUM) {
	    return compositeTaps_maximum(colors, states);
	}
	if (stepCompMode == COMP_MINIMUM) {
	    return compositeTaps_minimum(colors, states);
	}
	if (stepCompMode == COMP_MULTIPLY) {
	    return compositeTaps_multiply(colors, states);
	}
	if (stepCompMode == COMP_OUTSIDE) {
	    return compositeTaps_outside(colors, states);
	}
	if (stepCompMode == COMP_OVER) {
	    return compositeTaps_over(colors, states);
	}
	if (stepCompMode == COMP_SCREEN) {
	    return compositeTaps_screen(colors, states);
	}
	if (stepCompMode == COMP_SUBTRACT) {
	    return compositeTaps_subtract(colors, states);
	}
	if (stepCompMode == COMP_UNDER) {
	    return compositeTaps_under(colors, states);
	}
    return color;
}

out vec4 fragColor;
void main()
{
#if 0
    fragColor = vec4(float(tapFilterA[1]) / 7);
#else
    if (tapCount > 0) {
        bool[8] states = getTapStates();
        vec4[8] tapColors = getTaps(states);
        fragColor = compositeTaps(tapColors, states);
    } else {
        fragColor = texture(sTD3DInputs[0], vec3(vUV.st, W_OFFSET));
    }
#endif
}
