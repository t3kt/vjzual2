uniform int[4] tapActiveA;
uniform vec4 tapLengthA;
uniform vec4 tapAlphaA;
uniform int[4] tapFilterA;
uniform int[4] tapActiveB;
uniform vec4 tapLengthB;
uniform vec4 tapAlphaB;
uniform int[4] tapFilterB;
uniform int stepCompMode;
uniform int outputSelect;
uniform int tapCount;

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
	return texture(sTD3DInputs[0], vec3(vUV.st, length + W_OFFSET));
}

vec4[8] getTaps() {
    vec4[8] colors;
    for (int i = 0; i < 4; i++) {
        if (tapCount >= i && tapAlphaA[i] > 0.0) {
            colors[i] = applyFilter(getTap(tapLengthA[i], tapAlphaA[i]), tapFilterA[i]);
        } else {
            colors[i] = vec4(0.0);
        }
    }
    for (int i = 0; i < 4; i++) {
        if (tapCount >= (i + 4) && tapAlphaB[i] > 0.0) {
            colors[i + 4] = applyFilter(getTap(tapLengthB[i], tapAlphaB[i]), tapFilterB[i]);
        } else {
            colors[i + 4] = vec4(0.0);
        }
    }
    return colors;
}

vec4 compositeTaps_add(vec4[8] colors) {
    vec4 color = vec4(0.0);
    for (int i = 0; i < tapCount; i++) {
        color = color + colors[i];
    }
    return color;
}

vec4 compositeTaps_atop(vec4[8] colors) {
    vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
    for (int i = 0; i < tapCount; i++) {
        color = (color.rgba * colors[i].a) + (colors[i].rgba * (1.0 - color.a));
    }
    return color;
}

vec4 compositeTaps_difference(vec4[8] colors) {
    vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
    for (int i = 0; i < tapCount; i++) {
        color.rgb = abs(color.rgb - colors[i].rgb);
    }
    return color;
}

vec4 compositeTaps_inside(vec4[8] colors) {
    vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
    for (int i = 0; i < tapCount; i++) {
        color = color * clamp(colors[i], 0.0, 1.0);
    }
    return color;
}

vec4 compositeTaps_maximum(vec4[8] colors) {
    vec4 color = vec4(0.0);
    for (int i = 0; i < tapCount; i++) {
        color = max(color, colors[i]);
    }
    return color;
}

vec4 compositeTaps_minimum(vec4[8] colors) {
    vec4 color = vec4(1.0);
    for (int i = 0; i < tapCount; i++) {
        color = min(color, colors[i]);
    }
    return color;
}

vec4 compositeTaps_multiply(vec4[8] colors) {
    vec4 color = vec4(1.0);
    for (int i = 0; i < tapCount; i++) {
        color = color * colors[i];
    }
    return color;
}

vec4 compositeTaps_outside(vec4[8] colors) {
    vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
    for (int i = 0; i < tapCount; i++) {
        color = color * (1.0 - colors[i].a);
    }
    return color;
}

vec4 compositeTaps_over(vec4[8] colors) {
    vec4 color = vec4(0.0, 0.0, 0.0, 0.0);
    for (int i = 0; i < tapCount; i++) {
        color = (colors[i] * (1.0 - color.a)) + color;
    }
    return color;
}

vec4 compositeTaps_screen(vec4[8] colors) {
    vec4 color = vec4(0.0);
    for (int i = 0; i < tapCount; i++) {
        color = 1.0 - ((1.0 - color) * (1.0 - colors[i]));
    }
    return color;
}

vec4 compositeTaps_subtract(vec4[8] colors) {
    vec4 color = vec4(1.0);
    for (int i = 0; i < tapCount; i++) {
        color = color - colors[i];
    }
    return color;
}

vec4 compositeTaps_under(vec4[8] colors) {
    vec4 color = vec4(1.0);
    for (int i = 0; i < tapCount; i++) {
        color = (color * (1.0 - colors[i].a)) + colors[i];
    }
    return color;
}

vec4 compositeTaps(vec4[8] colors) {
	vec4 color = vec4(0.0);
	if (stepCompMode == COMP_ADD) {
	    return compositeTaps_add(colors);
	}
	if (stepCompMode == COMP_ATOP) {
	    return compositeTaps_atop(colors);
	}
	if (stepCompMode == COMP_AVERAGE) {
	    return compositeTaps_add(colors) / tapCount;
	}
	if (stepCompMode == COMP_DIFFERENCE) {
	    return compositeTaps_difference(colors);
	}
	if (stepCompMode == COMP_INSIDE) {
	    return compositeTaps_inside(colors);
	}
	if (stepCompMode == COMP_MAXIMUM) {
	    return compositeTaps_maximum(colors);
	}
	if (stepCompMode == COMP_MINIMUM) {
	    return compositeTaps_minimum(colors);
	}
	if (stepCompMode == COMP_MULTIPLY) {
	    return compositeTaps_multiply(colors);
	}
	if (stepCompMode == COMP_OUTSIDE) {
	    return compositeTaps_outside(colors);
	}
	if (stepCompMode == COMP_OVER) {
	    return compositeTaps_over(colors);
	}
	if (stepCompMode == COMP_SCREEN) {
	    return compositeTaps_screen(colors);
	}
	if (stepCompMode == COMP_SUBTRACT) {
	    return compositeTaps_subtract(colors);
	}
	if (stepCompMode == COMP_UNDER) {
	    return compositeTaps_under(colors);
	}
    return color;
}

out vec4 fragColor;
void main()
{
    if (tapCount > 0) {
        vec4[8] tapColors = getTaps();
        fragColor = compositeTaps(tapColors);
    } else {
        fragColor = texture(sTD3DInputs[0], vec3(vUV.st, W_OFFSET));
    }
}
