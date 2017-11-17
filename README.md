# fpfn-analysis

Each participant has its own folder inside `DATA`. Each participant folder is a "session" and has the following files:

- `gaze_coordenates.txt`
   - File containing participant's gaze points.

- `info.yml`
   - File containing participant's details about the experiment and the session. 

- `session_configuration.ini`
   - Configuration file of the Stimulus Control software used to generate the session.

- `session_events.txt`
   - File containing participant's behavioral events.

- `session_features.txt`
   - File containing locations of the distinctive stimulus.
   - The distinctive stimulus may be one of nine stimuli [1, 2 .. 9], `1` is the right most stimulus, clock-wise.
   - Stimuli size, stimuli position and screen size can be found in `/analysis/categorization/stimuli.py`
