
            document.addEventListener('DOMContentLoaded', function() {
                const form = document.querySelector('form');
                form.addEventListener('submit', async function(event) {
                    event.preventDefault();

                    const formData = new FormData(form);
                    try 
                    {
                        const response = await fetch('/', {
                            method: 'POST',
                            body: formData
                        });
                        if (response.ok) {
                            const result = await response.text();
                            document.getElementById('status').innerText = result;

                            // Display other information as needed
                            if (result.status === 'success') {
                                document.getElementById('optimized-sequence').innerText = result.optimized_sequence;
                                document.getElementById('optimized-cai').innerText = result.optimized_cai;
                            } 
                            else if (result.status === 'error') {
                                document.getElementById('error-message').innerText = result.message;
                            }
                        } 
                        else {
                            throw new Error('Failed to upload data');
                        }
                    }
                    catch (error){
                        console.error(error);
                        document.getElementById('status').innerText = 'Error uploading data';
                        document.getElementById('error-message').innerText = error.message;
                    }
                });
            });