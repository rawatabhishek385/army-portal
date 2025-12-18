# questions/forms.py

from django import forms
from .models import QuestionUpload, QuestionPaper
from reference.models import Trade
from .services import is_encrypted_dat, decrypt_dat_content, load_questions_from_excel_data

class QuestionUploadForm(forms.ModelForm):
    decryption_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter decryption password',
            'class': 'form-control'
        }),
        help_text="Password required for encrypted DAT files"
    )
    
    trade = forms.ModelChoiceField(
        queryset=Trade.objects.order_by('name'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Note: This field is for trade-specific papers only.",
        empty_label="-- Select Trade (Optional) --"
    )

    class Meta:
        model = QuestionUpload
        fields = ["file", "decryption_password", "trade"]
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("file")
        password = cleaned_data.get("decryption_password")

        if file and password:
            try:
                # Read file content into memory
                file.seek(0)
                file_content = file.read()
                file.seek(0)  # Reset file pointer

                # Basic validation - check if it looks like encrypted data
                if not is_encrypted_dat(file_content):
                    raise forms.ValidationError(
                        "File does not appear to be encrypted. Expected encrypted DAT file."
                    )

                # Test decryption with provided password
                try:
                    decrypted_data = decrypt_dat_content(file_content, password)
                    
                    # Verify it's a valid Excel file by checking magic bytes
                    if not decrypted_data.startswith(b'PK'):
                        raise forms.ValidationError(
                            "Decrypted data is not a valid Excel file format."
                        )
                    
                    # Try to parse the Excel data to validate structure
                    try:
                        questions = load_questions_from_excel_data(decrypted_data)
                        if not questions:
                            raise forms.ValidationError(
                                "No valid questions found in the Excel file."
                            )
                        
                        # Store for later use in signals
                        cleaned_data['validated_questions_count'] = len(questions)
                        
                    except Exception as e:
                        raise forms.ValidationError(
                            f"Error parsing Excel structure: {str(e)}"
                        )
                    
                except ValueError as e:
                    raise forms.ValidationError(
                        f"Decryption failed: {str(e)}. Please check your password."
                    )
                
                # Store file content for later use
                cleaned_data['file_content'] = file_content
                
            except forms.ValidationError:
                raise  # Re-raise form validation errors
            except Exception as e:
                raise forms.ValidationError(
                    f"Error processing file: {str(e)}"
                )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Set the password from form data
        if 'decryption_password' in self.cleaned_data:
            instance.decryption_password = self.cleaned_data['decryption_password']
        
        # Set the trade from form data
        instance.trade = self.cleaned_data.get('trade')
        
        if commit:
            instance.save()
        
        return instance


# ---------------------------------------------------------
# Admin ModelForm: QuestionPaperAdminForm
# The logic to disable the `trade` field for 'Secondary' papers is removed
# as 'Secondary' papers are no longer supported.
# ---------------------------------------------------------
class QuestionPaperAdminForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = '__all__'

    # The logic for 'Secondary' papers is removed.
    # The default form behavior is sufficient now that only 'Primary' exists.
    pass