import React, {useEffect, useState} from "react";
import '../styles/LayerUpload.scss';
import {
    Button, Checkbox,
    FormControl, FormControlLabel, FormGroup,
    Grid,
    InputLabel,
    MenuItem,
    Select,
    SelectChangeEvent,
    Stack,
    TextField,
    Typography
} from "@mui/material";


function HeaderComponent(props: any) {
    const [selectedLevel0, setSelectedLevel0] = useState<string>('');

    const handleLevel0Change = (event: SelectChangeEvent) => {
        setSelectedLevel0(event.target.value as string);
    }

    return (
        <div>
            <Grid container columnSpacing={2} className='header-container'>
                <Grid item xs={12} md={4} xl={3}>
                    <FormControl id="country-select-form">
                        <InputLabel id="country-select-label">Country</InputLabel>
                        <Select
                            labelId="country-select-label"
                            id="country-select"
                            value={selectedLevel0}
                            label="Country"
                            onChange={handleLevel0Change}
                        >
                            <MenuItem value={1}>Pakistan</MenuItem>
                            <MenuItem value={2}>Ukraine</MenuItem>
                            <MenuItem value={3}>Indonesia</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>
                <Grid item xs={12} md={8} xl={9}>
                    <Stack className='header-info'>
                        <Typography variant={'h6'}>
                            Last updated : 01.01.2018, source: HDX, ver: 1
                        </Typography>
                    </Stack>
                </Grid>
            </Grid>
        </div>
    )
}

interface LanguageOption {
    id: string,
    name: string
}

interface NameField {
    id: string,
    selectedLanguage: string,
    field: string,
    default: boolean,
}

function FormComponent() {

    const [languageOptions, setLanguageOptions] = useState<[] | LanguageOption[]>([])
    const [nameFields, setNameFields] = useState<NameField[]>([])

    const handleNameLanguageChange = (languageId: string, nameFieldId: string) => {
        const updatedNameFields = nameFields.map((nameField, index) => {
            if (nameField.id === nameFieldId) {
                nameField.selectedLanguage = languageId
            }
            return nameField
        })
        setNameFields(updatedNameFields);
    }

    const handleDefaultNameFieldChange = (event: SelectChangeEvent) => {
        let nameFieldId = event.target.value;
        const updatedNameFields = nameFields.map((nameField, index) => {
            nameField.default = nameField.id === nameFieldId;
            return nameField
        })
        setNameFields(updatedNameFields)
    }

    const addNameField = () => {
        let lastId = 0;
        for (const nameField of nameFields) {
            const nameFieldId = parseInt(nameField.id)
            if (lastId < nameFieldId) {
                lastId = nameFieldId
            }
        }
        lastId += 1
        setNameFields([
            ...nameFields,
            {
                id: lastId + '',
                selectedLanguage: '',
                field: '',
                default: false
            }
        ])
    }

    useEffect(() => {
        setLanguageOptions([
            {
                id: '1',
                name: 'English'
            },
            {
                id: '2',
                name: 'Indonesia'
            }
        ])
        setNameFields([{
            id: '1',
            selectedLanguage: '',
            field: '',
            default: false
        }])
        return
    },[])

    return (<div className='level-upload-container'>
        <Grid container columnSpacing={2}>
            <Grid item xl={6} md={6} xs={12}>
                <FormControl id="level-upload-form">
                    <Grid container columnSpacing={1}>
                        <Grid className={'form-label'} item md={4} xl={3} xs={12}>
                            <Typography variant={'subtitle1'}>Input file/URL</Typography>
                        </Grid>
                        <Grid item md={8} xl={9} xs={12}>
                            <TextField
                              id="outlined-uncontrolled"
                              label="Input file/URL"
                              defaultValue=""
                              sx={{ width: '100%' }}
                            />
                        </Grid>
                    </Grid>
                    <Grid container columnSpacing={1}>
                        <Grid className={'form-label'} item md={4} xl={3} xs={12}>
                            <Typography variant={'subtitle1'}>Location Type Field</Typography>
                        </Grid>
                        <Grid item md={8} xl={9} xs={12}>
                            <TextField
                              id="outlined-uncontrolled"
                              label="Location Type Field"
                              defaultValue=""
                              sx={{ width: '100%' }}
                            />
                        </Grid>
                    </Grid>

                    {nameFields.map((nameField: NameField, index: Number) => (
                        <Grid container columnSpacing={1} key={nameField.id}>
                            <Grid item className={'form-label'} md={4}
                                  xl={3} xs={12}>
                                {(index == 0) ? (
                                    <Typography variant={'subtitle1'}>Name
                                        Fields</Typography>
                                ) : null}
                            </Grid>

                            <Grid item md={8} xl={7} xs={12}>
                                <Grid container columnSpacing={1}
                                      style={{paddingBottom: 0}}>
                                    <Grid item md={6} xs={12}>
                                        <FormControl sx={{width: '100%'}}>
                                            <InputLabel
                                                id="language-select">Language</InputLabel>
                                            <Select
                                                labelId="language-label"
                                                className="language-select"
                                                value={nameField.selectedLanguage}
                                                label='Language'
                                                onChange={(event: SelectChangeEvent) => handleNameLanguageChange(
                                                    event.target.value as string, nameField.id)}
                                                style={{width: '100%'}}
                                            >
                                                {languageOptions.map((languageOption: LanguageOption) =>
                                                    <MenuItem
                                                        value={languageOption.id}
                                                        key={languageOption.id}>{languageOption.name}
                                                    </MenuItem>
                                                )}
                                            </Select>
                                        </FormControl>
                                    </Grid>
                                    <Grid item md={5} xs={12}>
                                        <TextField
                                            id="outlined-uncontrolled"
                                            label="Field"
                                            defaultValue=""
                                            disabled={nameField.selectedLanguage === ''}
                                            sx={{width: '100%'}}
                                        />
                                    </Grid>
                                    <Grid item md={1} xs={12}>
                                        <FormGroup className='default-check-box'>
                                          <FormControlLabel
                                              control={<Checkbox checked={nameField.default}
                                                                value={nameField.id}
                                                                onChange={handleDefaultNameFieldChange}/>}
                                              label="Default" />
                                        </FormGroup>
                                    </Grid>
                                </Grid>
                            </Grid>
                        </Grid>
                    ))}

                    <Grid container columnSpacing={1}>
                        <Grid item md={4} xl={3} xs={12}></Grid>
                        <Grid item>
                            <Button variant="contained" disableElevation onClick={addNameField}>
                                Add
                            </Button>
                        </Grid>
                    </Grid>
                </FormControl>
            </Grid>
        </Grid>

    </div>)
}


function LevelUpload() {
    return (
        <div>
            <HeaderComponent/>
            <FormComponent/>
        </div>
    )
}

export default LevelUpload;
